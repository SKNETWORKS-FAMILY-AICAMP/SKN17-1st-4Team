import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import mysql.connector
import matplotlib.pyplot as plt
import platform

plt.rc('font', family = 'Malgun Gothic')

#plt.rcParams['axes.unicode_minus'] = False

#DB 연결

def get_vehicle_density_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="skn_1st_4team",
        password="skn_1st_4team",
        database="densedb"
    )

    cursor = connection.cursor()

    sql = """
        SELECT month, city, district, passenger_car, van, truck, special, population
        FROM vehicle_density
    """

    cursor.execute(sql)
    result_rows = cursor.fetchall()

    # 컬럼명 설정
    columns = ['month', 'city', 'district', 'passenger_car', 'van', 'truck', 'special', 'population']
    
    # DataFrame 변환
    df = pd.DataFrame(result_rows, columns=columns)

    cursor.close()
    connection.close()

    return df

st.title("🗺️ 지역별 차량 밀집도 및 분석")

data = get_vehicle_density_data()
data = data[data['month'] != '2025-06']

vehicle_types = {
    "전체": ["passenger_car", "van", "truck", "special"],
    "승용차": ["passenger_car"],
    "밴": ["van"],
    "트럭": ["truck"],
    "특수차": ["special"]
}
selected_vehicle_type = st.selectbox("차량 종류 선택", options=vehicle_types, help="차량 종류를 선택하세요.")

months = data['month'].unique()
months = [m for m in months if m != '2025-06'] #6월 제외
selected_month = st.selectbox("월 선택", sorted(months, reverse = True))

def clean_city_name(name):
    correction_map = {
        '경산남도': '경상남도',
        '경산북도': '경상북도',
        '충천남도': '충청남도',
        '충천북도': '충청북도',
        '전북': '전라북도',
        '광주': '광주광역시',
        '대구': '대구광역시',
        '대전': '대전광역시',
        '부산': '부산광역시',
        '서울': '서울특별시',
        '울산': '울산광역시',
        '인천': '인천광역시',
        '세종': '세종특별자치시',
        '강원': '강원특별자치도',
        '제주': '제주특별자치도'
    }
    return correction_map.get(name, name)  

filtered = data[data['month'] == selected_month].copy()
filtered['city'] = filtered['city'].apply(clean_city_name)
filtered['selected_vehicle_sum'] = filtered[vehicle_types[selected_vehicle_type]].sum(axis=1)

grouped = (filtered.groupby('city', as_index=False).agg({
        'passenger_car': 'sum',
        'van': 'sum',
        'truck': 'sum',
        'special': 'sum',
        'population': 'sum'})
)

grouped['total_vehicle'] = filtered.groupby('city')[vehicle_types[selected_vehicle_type]].sum().sum(axis=1).values
#grouped['total_vehicle'] = grouped[['passenger_car', 'van', 'truck', 'special']].sum(axis=1)
grouped.rename(columns={'selected_vehicle_sum': 'total_vehicle'}, inplace=True)
grouped['density'] = grouped['total_vehicle'] / grouped['population']

coordinates = {
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '대구광역시': (35.8722, 128.6025),
    '인천광역시': (37.4563, 126.7052),
    '광주광역시': (35.1595, 126.8526),
    '대전광역시': (36.3504, 127.3845),
    '울산광역시': (35.5384, 129.3114),
    '세종특별자치시': (36.4801, 127.2890),
    '경기도': (37.4138, 127.5183),
    '강원특별자치도': (37.8228, 128.1555),
    '충청북도': (36.6358, 127.4913),
    '충청남도': (36.5184, 126.8000),
    '전라북도': (35.7167, 127.1442),
    '전라남도': (34.8161, 126.4630),
    '경상북도': (36.4919, 128.8889),
    '경상남도': (35.4606, 128.2132),
    '제주특별자치도': (33.4996, 126.5312)
}

m = folium.Map(location = [36.5, 127.8], zoom_start = 7)

def format_num_to_man(num):
    return f"{num/10000:.2f}만"

def get_color(density):
    if density < 0.3:
        return 'green'
    elif density < 0.6:
        return 'orange'
    else:
        return 'red'
    
TOP_N = 3
top_cities = grouped.nlargest(TOP_N, 'density')[['city', 'density']]

for idx, row in grouped.iterrows():
    city = row['city']
    if city in coordinates:
        folium.CircleMarker(
            location = coordinates[city],
            radius=row['density'] * 45,
            #radius = max(5, row['density'] * 50),
            popup=(f"{city}<br>"
                   f"차량: {format_num_to_man(row['total_vehicle'])}<br>"
                   f"인구:{format_num_to_man(row['population'])}<br>"
                   f"밀집도: {row['density']:.4f}"),
            color=get_color(row['density']),
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

# st.subheader(f"📍 {selected_month} 기준 차량 밀집도")
# st_folium(m, width=900, height=600)

# # 지도 바로 아래에 Top N 도시 출력
# st.markdown("---")
# st.subheader(f"🚩 차량 밀집도 Top {TOP_N}")
# for i, row in top_cities.iterrows():
#     st.write(f"**{row['city']}** — 밀집도: {row['density']:.4f}")

# 좌우 컬럼 나누기
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader(f"📍 {selected_month} 기준 차량 밀집도")
    st_folium(m, width=450, height=500)

with col2:
    st.subheader(f"🚩 밀집도 Top {TOP_N} 도시")
    for i, row in top_cities.iterrows():
        st.markdown(f"**{row['city']}**\n\n- 밀집도: {row['density']:.4f}")

# 전체 도시 밀집도 정렬표
st.subheader("📊 전체 도시 차량, 인구, 밀집도")
sorted_table = grouped[['city', 'total_vehicle', 'population', 'density']].copy()
sorted_table['차량 수'] = sorted_table['total_vehicle'].apply(lambda x: f"{int(x):,}")
sorted_table['인구 수'] = sorted_table['population'].apply(lambda x: f"{int(x):,}")
sorted_table['밀집도'] = sorted_table['density'].apply(lambda x: f"{x:.4f}")
sorted_table = sorted_table[['city', '차량 수', '인구 수', '밀집도']]
sorted_table = sorted_table.sort_values(by='밀집도', ascending=False).reset_index(drop=True)

st.dataframe(sorted_table, use_container_width=True)


# 월별 밀집도 변화 그래프 (전체 차량 기준)
data['city'] = data['city'].apply(clean_city_name)

# 전체 차량 종류 합산 컬럼 생성 (차종 필터 없이 전체 기준)
data['total_vehicle'] = data[['passenger_car', 'van', 'truck', 'special']].sum(axis=1)
data['density'] = data['total_vehicle'] / data['population']

# 월별 전국 평균 밀집도
monthly_density = data.groupby('month').apply(lambda df: df['total_vehicle'].sum() / df['population'].sum()).reset_index(name='avg_density')

st.subheader("📈 월별 전국 차량 밀집도 변화")
fig, ax = plt.subplots()
ax.plot(monthly_density['month'], monthly_density['avg_density'], marker='o')
ax.set_xlabel('월')
ax.set_ylabel('평균 밀집도 (차량/인구)')
ax.set_title('전국 월별 차량 밀집도 변화 추이')
ax.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig)
# 특정 기간 동안 차량이 얼마나 늘고 줄었는지 추세 파악. 특정 월에 밀집도 급증같은..

# # 차종별 밀집도 (월별 전체 합산)
# st.subheader("🚗 차종별 전국 밀집도 비교")
# vehicle_densities = {}
# for vt, cols in vehicle_types.items():
#     if vt == "전체":
#         continue
#     temp_df = data.groupby('month').apply(
#         lambda df: df[cols].sum().sum() / df['population'].sum()
#     ).reset_index(name='density')
#     vehicle_densities[vt] = temp_df

# fig2, ax2 = plt.subplots()
# for vt, df_vt in vehicle_densities.items():
#     ax2.plot(df_vt['month'], df_vt['density'], marker='o', label=vt)
# ax2.set_xlabel('월')
# ax2.set_ylabel('평균 밀집도')
# ax2.set_title('차종별 월별 평균 차량 밀집도')
# ax2.legend()
# ax2.grid(True)
# plt.xticks(rotation=45)
# st.pyplot(fig2)

# 상위 N 도시 밀집도 변화 추세
TOP_N = 5
top_cities_all = data.groupby('city').apply(
    lambda df: df['total_vehicle'].sum() / df['population'].sum()
).sort_values(ascending=False).head(TOP_N).index.tolist()

st.subheader(f"🏙️ 밀집도 상위 {TOP_N} 도시 월별 변화 추이")
fig3, ax3 = plt.subplots()
for city in top_cities_all:
    city_df = data[data['city'] == city]
    city_monthly_density = city_df.groupby('month').apply(
        lambda df: df['total_vehicle'].sum() / df['population'].sum()
    ).reset_index(name='density')
    ax3.plot(city_monthly_density['month'], city_monthly_density['density'], marker='o', label=city)
ax3.set_xlabel('월')
ax3.set_ylabel('밀집도')
ax3.set_title(f'상위 {TOP_N} 도시 밀집도 변화 추세')
ax3.legend()
ax3.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig3)

### --- 4. 밀집도 기반 코멘트 --- ###
st.subheader("💬 지역별 밀집도 인사이트")

def density_comment(density):
    if density >= 0.6:
        return "차량 밀집도가 매우 높습니다. 주차장 부족과 교통 혼잡 문제가 예상됩니다."
    elif density >= 0.3:
        return "차량 밀집도가 보통 수준으로, 교통 인프라 점검이 필요합니다."
    else:
        return "차량 밀집도가 낮아 여유로운 편입니다."

# 선택한 월과 차종 기준 밀집도 상위 5개 도시
top5_cities = grouped.nlargest(5, 'density')

for idx, row in top5_cities.iterrows():
    st.write(f"**{row['city']}** - 밀집도: {row['density']:.4f}")
    st.write(density_comment(row['density']))
    st.write("---")