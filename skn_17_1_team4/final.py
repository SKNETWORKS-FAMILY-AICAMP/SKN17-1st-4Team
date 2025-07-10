import os
import re
import pandas as pd
import pymysql

### 1. 표준화 함수
def std_month(x):
    # '2025-4' -> '2025-04', '2025-12' -> '2025-12'
    if '-' in x:
        y, m = x.split('-')
        return f"{y}-{int(m):02d}"
    return x

def std_district(x):
    # 한글, 숫자만 남기고 공백/기타 문자 삭제, ex) ' 강남 구 ' -> '강남구'
    return re.sub(r'[^가-힣0-9]', '', str(x))

### 2. 자동차 데이터 함수
def get_car_result():
    folder_path = "excel"
    sheet_name = '02.통계표_시군구'
    car_result = []
    for file_name in os.listdir(folder_path):
        if not file_name.endswith('_car.xlsx'):
            continue
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        raw_month = str(df.iloc[1, 1])
        if '.' in raw_month:
            year, month = raw_month.split('.')
            month = str(int(month)).zfill(2)
            조회년월 = f"{year}-{month}"
        else:
            조회년월 = raw_month
        for idx in range(len(df)):
            row = df.iloc[idx]
            시군구 = str(row[1])
            if (시군구.endswith(('구', '시', '군'))
                and '합계' not in 시군구
                and '소계' not in 시군구
                and 시군구 != 'nan'
                and not 시군구.isdigit()):
                item = {
                    'month': std_month(조회년월),
                    'district': std_district(시군구),
                    'passenger_car': int(str(row[5]).replace(',', '')) if not pd.isna(row[5]) else 0,
                    'van': int(str(row[9]).replace(',', '')) if not pd.isna(row[9]) else 0,
                    'truck': int(str(row[13]).replace(',', '')) if not pd.isna(row[13]) else 0,
                    'special': int(str(row[17]).replace(',', '')) if not pd.isna(row[17]) else 0,
                }
                car_result.append(item)
    return car_result

### 3. 인구 데이터 함수
def get_population_result():
    folder_path = "population"
    sido_list = ['강원도', '경기도', '경산남도', '경산북도', '광주', '대구', '대전', '부산', '서울', '세종', '울산', '인천', '전라남도', '전북', '제주도', '충천남도', '충천북도']
    pop_result = []
    for sido_name in sido_list:
        file_path = os.path.join(folder_path, f"{sido_name}.xlsx")
        if not os.path.exists(file_path):
            print(f"{file_path} 파일이 존재하지 않습니다.")
            continue
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        month_row = df.iloc[1]
        month_indices = [i for i, x in enumerate(month_row) if pd.notna(x) and "월" in str(x)]
        for month_idx in month_indices:
            raw_month = str(df.iloc[1, month_idx]).replace(" ", "")
            year = raw_month[:4]
            month = str(int(raw_month[5:7])).zfill(2)
            조회년월 = f"{year}-{month}"
            for row_idx in range(4, len(df)):
                시군구 = str(df.iloc[row_idx, 1])
                인구값 = df.iloc[row_idx, month_idx]
                # 모든 시도명, 공백 제거
                시군구명 = (
                    시군구
                    .replace("서울특별시", "")
                    .replace("강원특별자치도", "")
                    .replace("강원도", "")
                    .replace("경기도", "")
                    .replace("경상남도", "")
                    .replace("경상북도", "")
                    .replace("경산남도", "")
                    .replace("경산북도", "")
                    .replace("광주광역시", "")
                    .replace("부산광역시", "")
                    .replace("대구광역시", "")
                    .replace("대전광역시", "")
                    .replace("울산광역시", "")
                    .replace("인천광역시", "")
                    .replace("전북특별자치도", "")
                    .replace("전북특별자치시", "")
                    .replace("전라남도", "")
                    .replace("전라북도", "")
                    .replace("충청남도", "")
                    .replace("충청북도", "")
                    .replace("충천남도", "")
                    .replace("충천북도", "")
                    .replace("세종특별자치시", "")
                    .replace("제주특별자치도", "")
                    .replace("제주도", "")
                    .replace(" ", "")
                )
                match = re.search(r'([가-힣]+구)$', 시군구명)
                if match and pd.notna(인구값):
                    district = std_district(match.group(1))
                    item = {
                        'month': std_month(조회년월),
                        'city': sido_name,
                        'district': district,
                        'population': int(str(인구값).replace(",", "")),
                    }
                    pop_result.append(item)
    return pop_result

### 4. 데이터 추출 및 표준화
car_data = get_car_result()
pop_data = get_population_result()
df_car = pd.DataFrame(car_data)
df_pop = pd.DataFrame(pop_data)

# 표준화 (한 번 더 안전하게!)
df_car['district'] = df_car['district'].apply(std_district)
df_pop['district'] = df_pop['district'].apply(std_district)
df_car['month'] = df_car['month'].apply(std_month)
df_pop['month'] = df_pop['month'].apply(std_month)

### 5. 인구 데이터 기준으로 병합!
df_merge = pd.merge(
    df_pop, df_car,
    on=['month', 'district'],
    how='left'
)
# 자동차 데이터 없는 곳은 0으로 채우기
for col in ['passenger_car', 'van', 'truck', 'special']:
    if col in df_merge.columns:
        df_merge[col] = df_merge[col].fillna(0).astype(int)
    else:
        df_merge[col] = 0

# population, city는 인구데이터 기준이라 항상 존재

### 6. 누락 데이터 확인(자동차 데이터 없는 곳만 나옴)
missing = df_merge[(df_merge['passenger_car'] == 0) &
                   (df_merge['van'] == 0) &
                   (df_merge['truck'] == 0) &
                   (df_merge['special'] == 0)]
if len(missing) > 0:
    print("※ 자동차 데이터 없는 행 (참고):")
    print(missing[['month', 'city', 'district', 'population']])

### 7. MySQL 저장
conn = pymysql.connect(
    host='localhost',
    user='skn_1st_4team',
    password='skn_1st_4team',  # 본인 DB비번
    db='densedb',  # 본인 DB명
    charset='utf8mb4'
)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS vehicle_density (
    month VARCHAR(7) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    passenger_car INT NOT NULL,
    van INT NOT NULL,
    truck INT NOT NULL,
    special INT NOT NULL,
    population INT,
    PRIMARY KEY (month, city, district)
) ENGINE=InnoDB COMMENT '자동차 및 인구 현황';
""")

for _, row in df_merge.iterrows():
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
    values = (
        row['month'],
        row['city'],
        row['district'],
        int(row['passenger_car']),
        int(row['van']),
        int(row['truck']),
        int(row['special']),
        int(row['population'])
    )
    cur.execute(sql, values)

conn.commit()
cur.close()
conn.close()
print("모든 데이터 저장 완료!")
