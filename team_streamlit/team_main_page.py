import streamlit as st

st.header('SKN17-1st-4Team 🔗연결담')
st.subheader('지역별 차량 밀집도 기반 플랫폼 및 기업별 FAQ 조회 시스템')

st.markdown(':blue-background[🗒️목차]')
st.page_link("pages/1_dense.py", label = "차량등록 밀도", icon = "🚗")
st.page_link("pages/2_faq.py", label = "기업별 FAQ", icon = "🤔")