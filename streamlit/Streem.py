import streamlit as st
import pandas as pd
import requests

# 페이지 설정
st.set_page_config(page_title="전국 자동차 등록 현황 및 기업별 FAQ", layout="wide")

# 앱 제목
st.title("🚗 전국 자동차 등록 현황 및 기업별 FAQ")

# 사이드바 메뉴
menu = st.sidebar.selectbox("메뉴 선택", ["차량 등록 조회", "기업 FAQ"])

# ------------------------------
# 차량 등록 조회 메뉴 (API 호출)
# ------------------------------
if menu == "차량 등록 조회":
    st.header("📊 월별 차량 등록 현황 조회")

    selected_month = st.selectbox(
        "조회할 월을 선택하세요",
        options=pd.date_range("2023-01-01", "2025-12-01", freq="MS").strftime("%Y-%m"),
        index=len(pd.date_range("2023-01-01", "2025-12-01", freq="MS")) - 1
    )

    if st.button("조회"):
        try:
            response = requests.get(
                "http://localhost:8000/vehicle",
                params={"month": selected_month}
            )
            response.raise_for_status()
            data = response.json()

            st.success(f"{selected_month} 등록 현황 조회 성공 ✅")

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

    # 세션 상태 초기화
    if "faq_data" not in st.session_state:
        st.session_state.faq_data = None
        st.session_state.data_loaded = False
    if "selected_company" not in st.session_state:
        st.session_state.selected_company = "기아"
    if "search_query_question" not in st.session_state:
        st.session_state.search_query_question = ""
    if "search_query_answer" not in st.session_state:
        st.session_state.search_query_answer = ""

    # 기업 선택
    selected_company = st.selectbox(
        "기업 선택", ["기아", "현대"],
        index=["기아", "현대"].index(st.session_state.selected_company),
        key="company_select"
    )

    # FAQ 조회 버튼
    if st.button("FAQ 조회"):
        try:
            csv_file = "kia_faq.csv" if selected_company == "기아" else "hyundai_all.csv"
            df = pd.read_csv(csv_file, encoding="utf-8-sig")
            df_sorted = df.sort_values(by=df.columns[0], ascending=True, ignore_index=True)

            # 상태 저장
            st.session_state.faq_data = df_sorted
            st.session_state.data_loaded = True
            st.session_state.selected_company = selected_company

            st.success(f"{selected_company} FAQ 데이터 로드 완료 ✅")

        except FileNotFoundError:
            st.error(f"{csv_file} 파일이 존재하지 않습니다.")
        except Exception as e:
            st.error(f"FAQ 로드 중 오류 발생: {e}")

    # 🔄 초기화 버튼
    if st.button("🔄 초기화"):
        st.session_state.faq_data = None
        st.session_state.data_loaded = False
        st.session_state.selected_company = "기아"
        st.session_state.search_query_question = ""
        st.session_state.search_query_answer = ""
        st.rerun()

    # 데이터가 로드된 경우
    if st.session_state.data_loaded and st.session_state.faq_data is not None:
        full_df = st.session_state.faq_data
        question_col = full_df.columns[0]
        answer_col = full_df.columns[1]

        # 🔍 검색 입력창 (즉시 반영 방식 - key만 사용)
        st.markdown("### ❓ 질문 기준 FAQ 검색")
        st.text_input("질문 키워드", key="search_query_question")

        st.markdown("### 💬 답변 기준 FAQ 검색")
        st.text_input("답변 키워드", key="search_query_answer")

        # 검색 키워드 가져오기
        q_keyword = st.session_state.search_query_question.strip()
        a_keyword = st.session_state.search_query_answer.strip()

        # 필터링 처리
        filtered_df = full_df.copy()
        if q_keyword:
            filtered_df = filtered_df[filtered_df[question_col].astype(str).str.contains(q_keyword, case=False, na=False)]
        if a_keyword:
            filtered_df = filtered_df[filtered_df[answer_col].astype(str).str.contains(a_keyword, case=False, na=False)]

        # 결과 출력
        if q_keyword or a_keyword:
            if not filtered_df.empty:
                st.markdown("### 🔍 검색 결과")
                st.dataframe(filtered_df.sort_values(by=question_col), use_container_width=True, height=600)

                st.download_button(
                    label="🔽 검색 결과 다운로드 (CSV)",
                    data=filtered_df.to_csv(index=False, encoding='utf-8-sig'),
                    file_name=f"{selected_company}_faq_filtered.csv",
                    mime='text/csv'
                )
            else:
                st.warning("검색 결과가 없습니다.")
        else:
            # 전체 보기
            st.markdown("### 📄 전체 FAQ 보기 (가나다순)")
            st.dataframe(full_df, use_container_width=True, height=900)

            st.download_button(
                label=f"🔽 {selected_company} FAQ 전체 다운로드 (CSV)",
                data=full_df.to_csv(index=False, encoding='utf-8-sig'),
                file_name=f"{selected_company}_faq.csv",
                mime='text/csv'
            )

