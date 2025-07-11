import streamlit as st
import pandas as pd

st.header('🚘기업별 FAQ 조회')

#회사 선택
select_company = st.selectbox("기업 선택", ["선택","현대", "기아"])

df_hyundai = pd.read_csv("hyundai_all_new.csv")
df_kia = pd.read_csv("kia_faq_all_final_new.csv")
df = pd.concat([df_hyundai, df_kia], ignore_index=True)

keyword = st.text_input("검색할 키워드를 입력하세요", "")

#기업 필터링
if select_company != "선택":
    filtered_df = df[df["기업명"] == select_company]
else:
    filtered_df = df.copy()

#키워드 필터링
if keyword:
    filtered_df = filtered_df[
        filtered_df["질문"].str.contains(keyword, case=False, na=False) |
        filtered_df["답변"].str.contains(keyword, case=False, na=False) 
    ]
else:
    filtered_df = df[df["기업명"] == select_company]

st.write(f"🔎 총 {len(filtered_df)}건의 결과가 있습니다.")


#결과 출력
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        with st.expander(f"{row['기업명']} | {row['질문ID']} | {row['질문']}"):
            st.write(row["답변"])
else:
    st.warning("해당 조건에 맞는 FAQ가 없습니다.")