# SKN17-1st-4Team
<div align="center">
  <h1>지역별 차량 밀집도 기반 플랫폼 및 기업별 FAQ 조회 시스템</h1>
  <p>🔗 연결담 🔗</p>
</div>

## 팀 소개
### ✅ 팀 명
SKN17-1st-4Team : 🔗 연결담 🔗
### 🧑‍💻 팀 멤버
| 이름    | 역할        | 
|:-----------:|:---------------:|
| 양정민      | Streamlit 코드 작성           | 
| 조해리      | 기업별 FAQ 크롤링 및 처리, Readme 작성|
| 김준협      | python을 이용한 excel 데이터 가공  |
| 이재은      | ERD설계, 현대 FAQ 크롤링, Readme 작성|
---
## 지역별 차량 밀집도 기반 플랫폼 및 기업별 FAQ 조회 시스템
### 🗓️ 프로젝트 기간
✔️ 2025.07.10 ~ 2025.07.11
### 📖 프로젝트 소개

- 전국 자동차 등록 데이터를 바탕으로 지역별 차량 밀집도를 분석하여,

  **소비자**, **기업**, **지자체**, **정책 담당자** 등 다양한 사용자들이 

  실질적인 판단과 의사 결정을 내릴 수 있는 인사이트를 제공하는 프로젝트

### 📌 프로젝트 필요성 (배경)

- 차량 수가 증가함에 따라 **주차, 교통 혼잡, 충전소 부족** 등 도시 문제가 심화되고 있음
- 등록 차량 데이터는 공개되어 있으나, **직관적인 분석과 시각화 도구 부족**
- 이를 해결하기 위해, **누구나 쉽게 차량 분포를 조회**하고 **필요한 인프라나 정책 수립에 도움을 주는 플랫폼**이 필요함
    

### 🎯 프로젝트 목표

- 지역별 차량 밀집도 및 등록 현황 시각화
- 연료별, 차종별, 등록연도별 필터 제공
- 각 사용자 유형에 맞춘 **활용 코멘트** 제공 (소비자/기업/지자체)
- 행정구 단위 비교 및 의사 결정 도우미 기능
- 기업별 FAQ 조회

### 기술 스택
- <img src="https://img.shields.io/badge/Python-3776AB?style=plastic&logo=Python&logoColor=white">
- <img src="https://img.shields.io/badge/MySQL-4479A1?style=plastic&logo=MySQL&logoColor=white">
- <img src="https://img.shields.io/badge/pandas-150458?style=plastic&logo=pandas&logoColor=white">
- <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=plastic&logo=streamlit&logoColor=white">
- <img src="https://img.shields.io/badge/git-F05032?style=plastic&logo=git&logoColor=white">
- <img src="https://img.shields.io/badge/github-181717?style=plastic&logo=github&logoColor=white">
- <img src="https://img.shields.io/badge/selenium-43B02A?style=plastic&logo=selenium&logoColor=white">

### WBS
| 단계 | 설명 |
| --- | --- |
| 🧩 **1. 데이터 수집 및 전처리** | - 차량 등록 수, 인구, 면적 등 공공 데이터 수집                     - 지역별 차량 밀집도 계산 (등록 수 / 면적) |
| 🗂️ **2. ERD 설계 및 DB 구축** | - 관계형 데이터베이스 설계 (ERD)                                          - 차량 등록, 지역, 인구, 밀집도 등 테이블 생성 |
| 🤖 **3. 웹 크롤링 (FAQ 수집)** | - Selenium 활용하여 현대, 기아 FAQ 수집                             - 질문·답변 구조화 후 DB에 저장 |
| 💻 **4. 웹사이트 구현** | - 차트/지도 기반 시각화 (차량 밀집도 등)                             - 필터 기능 (지역, 차종, 연료 등)                                             - 사용자 맞춤형 코멘트 제공 |
| 📄 **5. 문서화 및 발표 자료 준비** | - README, ERD, WBS 정리                                                    - 시연 및 발표 자료 구성 |

### 요구 사항 명세서

| 기능 | 설명 |
| --- | --- |
| 지역 선택 | 시/도 및 구 단위 지역 선택 |
| 필터 | 연도, 차종, 연료 등 선택 필터 |
| 시각화 | 차량 수, 차량 밀도(대/km²) 차트/지도 |
| 활용 코멘트 | 소비자/기업/지자체용 인사이트 문장 제공 |

### ERD

<img width="500" height="239" alt="Image" src="https://github.com/user-attachments/assets/a07440b5-0512-4731-b00a-2edc019446d2" />
