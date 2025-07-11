import os
import re
import pandas as pd
import pymysql

def remove_sido_prefix(name):
    if pd.isna(name):
        return ""
    name = str(name).strip()
    # 긴 시도명칭 우선
    pattern = r'^(전북특별자치도|전북특별자치시|전남특별자치도|강원특별자치도|제주특별자치도|서울특별시|부산광역시|대구광역시|인천광역시|광주광역시|대전광역시|울산광역시|세종특별자치시|경기도|강원도|충청북도|충북|충청남도|충남|전라북도|전북|전라남도|전남|경상북도|경북|경상남도|경남|제주도|제주)\s*'
    return re.sub(pattern, '', name)

def get_pop_data_from_file(filepath):
    df = pd.read_excel(filepath, header=None)
    month_row = df.iloc[1]
    month_indices = [i for i, x in enumerate(month_row) if pd.notna(x) and "월" in str(x)]
    results = []
    # city = 시도(예: 경기, 강원...)는 파일명에서 추출
    city = os.path.basename(filepath).split('_')[2].replace('.xlsx', '').replace('pop', '').replace(' ', '')
    for month_idx in month_indices:
        raw_month = str(df.iloc[1, month_idx]).replace(" ", "")
        year = raw_month[:4]
        month = str(int(raw_month[5:7])).zfill(2)
        조회년월 = f"{year}-{month}"
        for row_idx in range(5, len(df)):
            시군구 = df.iloc[row_idx, 1]
            인구값 = df.iloc[row_idx, month_idx]
            if pd.notna(시군구) and pd.notna(인구값):
                district = remove_sido_prefix(시군구)
                # "수원시 장안구"처럼 '구', '군', '시'로 끝나는 것만
                if district and district[-1] in '군구시':
                    results.append({
                        "month": 조회년월,
                        "city": city,
                        "district": district,
                        "population": int(str(인구값).replace(',', ''))
                    })
    return results

def get_car_data_from_file(filepath):
    df = pd.read_excel(filepath, sheet_name='02.통계표_시군구', header=None)
    raw_month = str(df.iloc[1, 1])
    if '.' in raw_month:
        year, month = raw_month.split('.')
        month = str(int(month)).zfill(2)
        조회년월 = f"{year}-{month}"
    else:
        조회년월 = raw_month
    results = []
    for idx in range(4, len(df)):
        시군구 = df.iloc[idx, 1]
        if pd.isna(시군구):
            continue
        district = str(시군구).strip()  # 그대로 사용
        # '구', '군', '시'로 끝나는 행만
        if not district or district[-1] not in '군구시':
            continue
        # 시도(도, 광역시 등)는 df.iloc[idx,0]에 있으나 PK는 district만 쓸거라 별도 활용 X
        item = {
            "month": 조회년월,
            "city": '',  # 필요시 district에서 유추 가능
            "district": district,
            "passenger_car": int(str(df.iloc[idx, 5]).replace(',', '')) if not pd.isna(df.iloc[idx, 5]) else 0,
            "van": int(str(df.iloc[idx, 9]).replace(',', '')) if not pd.isna(df.iloc[idx, 9]) else 0,
            "truck": int(str(df.iloc[idx, 13]).replace(',', '')) if not pd.isna(df.iloc[idx, 13]) else 0,
            "special": int(str(df.iloc[idx, 17]).replace(',', '')) if not pd.isna(df.iloc[idx, 17]) else 0,
        }
        results.append(item)
    return results

def get_all_pop_data(pop_folder):
    all_results = []
    for file_name in os.listdir(pop_folder):
        if file_name.endswith('_pop.xlsx'):
            file_path = os.path.join(pop_folder, file_name)
            all_results += get_pop_data_from_file(file_path)
    return all_results

def get_all_car_data(car_folder):
    all_results = []
    for file_name in os.listdir(car_folder):
        if file_name.endswith('_car.xlsx'):
            file_path = os.path.join(car_folder, file_name)
            all_results += get_car_data_from_file(file_path)
    return all_results

### 경로 지정
pop_folder = 'population'
car_folder = 'excel'

### 데이터 추출
pop_data = get_all_pop_data(pop_folder)
car_data = get_all_car_data(car_folder)

pop_df = pd.DataFrame(pop_data)
car_df = pd.DataFrame(car_data)

# 병합(중복 컬럼 삭제)
merged = pd.merge(
    pop_df, car_df[['month', 'district', 'passenger_car', 'van', 'truck', 'special']],
    on=['month', 'district'],
    how='left'
)
for col in ['passenger_car', 'van', 'truck', 'special']:
    merged[col] = merged[col].fillna(0).astype(int)

print(merged.head(20))

### MySQL insert는 district만 PK로 저장 (city는 값 필요시 district에서 추출)
# 예시:
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='skn_1st_4team',
    password='skn_1st_4team',
    db='densedb'
)
cur = conn.cursor()
for _, row in merged.iterrows():
    sql = """
        INSERT INTO vehicle_density
        (month, city, district, passenger_car, van, truck, special, population)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            passenger_car=VALUES(passenger_car),
            van=VALUES(van),
            truck=VALUES(truck),
            special=VALUES(special),
            population=VALUES(population)
    """
    cur.execute(sql, (
        row['month'], row['city'], row['district'], row['passenger_car'],
        row['van'], row['truck'], row['special'], row['population']
    ))
conn.commit()
cur.close()
conn.close()
print('DB 저장 완료!')
