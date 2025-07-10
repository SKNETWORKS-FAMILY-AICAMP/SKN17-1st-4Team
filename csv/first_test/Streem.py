import streamlit as st
import pandas as pd
import requests
import math

# 페이지 설정
st.set_page_config(page_title="전국 자동차 등록 현황 및 기업별 FAQ", layout="wide")

# 앱 제목
st.title("🚗 전국 자동차 등록 현황 및 기업별 FAQ")

# 사이드바 메뉴 선택
menu = st.sidebar.selectbox("메뉴 선택", ["차량 등록 조회", "기업 FAQ"])

# ------------------------------
# 차량 등록 조회 메뉴 (월별)
# ------------------------------
if menu == "차량 등록 조회":
    st.header("📊 월별 차량 등록 현황 조회")

    # 월 선택
    selected_month = st.selectbox(
        "조회할 월을 선택하세요",
        options=pd.date_range("2023-01-01", "2025-12-01", freq="MS").strftime("%Y-%m"),
        index=len(pd.date_range("2023-01-01", "2025-12-01", freq="MS")) - 1
    )

    if st.button("조회"):
        try:
            # API 요청
            response = requests.get(
                "http://localhost:8000/vehicle",
                params={"month": selected_month}
            )
            response.raise_for_status()
            data = response.json()

            st.success(f"{selected_month} 등록 현황 조회 성공 ✅")

            # DataFrame 변환
            df = pd.DataFrame(data)

            if df.empty:
                st.warning("해당 월의 데이터가 없습니다.")
            else:
                st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"조회 실패: {e}")

# ------------------------------
# 기업 FAQ 메뉴
# ------------------------------
elif menu == "기업 FAQ":
    st.header("🏢 기업별 FAQ 조회")

    # 기업 선택
    selected_company = st.selectbox("기업 선택", ["기아", "현대"], key="company_select")

    # 세션 상태 초기화
    if "faq_data" not in st.session_state:
        st.session_state.faq_data = None
        st.session_state.data_loaded = False

    if st.button("FAQ 조회"):
        try:
            csv_file = "kia_faq.csv" if selected_company == "기아" else "hyundai_all.csv"
            df = pd.read_csv(csv_file, encoding="utf-8-sig")

            # 첫 번째 열 기준 가나다 정렬
            first_col = df.columns[0]
            df_sorted = df.sort_values(by=first_col, ascending=True, ignore_index=True)

            # 세션 상태에 저장
            st.session_state.faq_data = df_sorted
            st.session_state.data_loaded = True
            st.success(f"{selected_company} FAQ 데이터 로드 완료 ✅ (가나다순 정렬됨)")

        except FileNotFoundError:
            st.error(f"{csv_file} 파일이 존재하지 않습니다. 먼저 크롤링을 수행해주세요.")
        except Exception as e:
            st.error(f"FAQ 로드 중 오류 발생: {e}")

    # 데이터가 로드된 경우
    if st.session_state.data_loaded and st.session_state.faq_data is not None:
        df = st.session_state.faq_data

        st.markdown("### 📄 가나다순 FAQ 전체 보기")
        st.dataframe(df, use_container_width=True, height=900)

        # CSV 다운로드
        st.download_button(
            label=f"{selected_company} FAQ 다운로드 (CSV)",
            data=df.to_csv(index=False, encoding='utf-8-sig'),
            file_name=f"{selected_company}_faq.csv",
            mime='text/csv'
        )
