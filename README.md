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

- 전국 자동차 등록 데이터를 바탕으로 지역별 차량 등록 밀집도를 시각적으로 분석하여,

   **기업**, **지자체**, **정책 담당자** 등 다양한 사용자들이 

  실질적인 판단과 의사 결정을 내릴 수 있는 인사이트를 제공하는 프로젝트

- 기업별 FAQ 조회 시스템을 통해 고객 문의에 대한 신속하고
  효율적인 정보 제공을 도모

### 📌 프로젝트 필요성 (배경)

- 차량 수가 증가함에 따라 **주차, 교통 혼잡, 충전소 부족** 등 도시 문제가 심화되고 있음
  
<img width="500" height="55" alt="Image" src="https://github.com/user-attachments/assets/23d78fdf-c3d1-4d26-8d5e-f3ab83dc43b2" /> 

<img width="500" height="208" alt="Image" src="https://github.com/user-attachments/assets/dfd5f351-cc7c-48cf-a74e-bd81009da082" />

<img width="550" height="305" alt="Image" src="https://github.com/user-attachments/assets/b60b4d04-292f-44ad-9ea5-a8c64e4ed2c3" />


<img width="300" height="115" alt="image" src="https://github.com/user-attachments/assets/e2c17f8d-f35e-480b-b78e-6e556ccbd23a" />


<img width="300" height="176" alt="image" src="https://github.com/user-attachments/assets/2119fa14-c58a-44fd-bfc8-bc5ab723be29" />

<img width="500" height="199" alt="image" src="https://github.com/user-attachments/assets/c8b3526d-ead8-4e7d-baec-91799f85f825" />

<img width="500" height="247" alt="image" src="https://github.com/user-attachments/assets/cb86268f-2d5c-46d1-8e01-ae7279bdfbb6" />




- 등록 차량 데이터는 공개되어 있으나, **직관적인 분석과 시각화 도구 부족**
- 이를 해결하기 위해, **누구나 쉽게 차량 분포를 조회**하고 **필요한 인프라나 정책 수립에 도움을 주는 플랫폼**이 필요함
- 기업 FAQ를 함께 참고할 수 있는 종합 정보 플랫폼의 필요성 대두
    

### 🎯 프로젝트 목표
  
- 차종별, 등록연도별, 월별 필터 -> 차량 밀집도 지도를 통한 시각화
- 월별 Top 3 밀집도 도시, 도시별 차량,인구,밀집도 데이터 제공
- 월별 전국 차량 밀집도 변화 그래프 제공
- 월별 TOP 5 밀집도 변화 그래프 제공
- 기업별 FAQ 조회, 키워드 검색 기능

### 기술 스택
- <img src="https://img.shields.io/badge/Python-3776AB?style=plastic&logo=Python&logoColor=white">
- <img src="https://img.shields.io/badge/MySQL-4479A1?style=plastic&logo=MySQL&logoColor=white">
- <img src="https://img.shields.io/badge/pandas-150458?style=plastic&logo=pandas&logoColor=white">
- <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=plastic&logo=streamlit&logoColor=white">
- <img src="https://img.shields.io/badge/git-F05032?style=plastic&logo=git&logoColor=white">
- <img src="https://img.shields.io/badge/github-181717?style=plastic&logo=github&logoColor=white">
- <img src="https://img.shields.io/badge/selenium-43B02A?style=plastic&logo=selenium&logoColor=white">

### WBS
| 단계 | 설명 | 일정 |
| --- | --- | --- |
| 🧩 **1. 데이터 수집 및 전처리** | - 차량 등록 수, 인구, 면적 등 공공 데이터 수집<br>- 지역별 차량 밀집도 계산 (등록 수 / 면적) | 7/10 |
| 🗂️ **2. ERD 설계 및 DB 구축** | - 관계형 데이터베이스 설계 (ERD)<br>- 차량 등록, 지역, 인구, 밀집도 등 테이블 생성 | 7/10 ~ 7/11 |
| 🤖 **3. 웹 크롤링 (FAQ 수집)** | - Selenium 활용하여 현대, 기아 FAQ 수집<br>- 질문·답변 구조화 후 DB에 저장 | 7/10 |
| 💻 **4. 웹사이트 구현** | - 차트/지도 기반 시각화 (차량 밀집도 등)<br>- 필터 기능 (지역, 차종, 연료 등)<br>- 사용자 맞춤형 코멘트 제공 | 7/11 |
| 📄 **5. 문서화 및 발표 자료 준비** | - README, ERD, WBS 정리<br>- 시연 및 발표 자료 구성 | 7/11 |


### 요구 사항 명세서

| 기능       | 설명                                                         |
|------------|--------------------------------------------------------------|
| 지역 선택  | 시/도 및 구 단위로 지역을 선택하여 데이터 조회 가능             |
| 필터       | 연도별, 차종별(승용차, SUV, 트럭 등), 연료 종류(가솔린, 전기 등)로 상세 필터링 지원 |
| 시각화     | 차량 등록 수와 차량 밀집도(대/명)를 차트(막대, 히스토그램) 및 지도 기반으로 시각화 |
| 기업 FAQ   | 현대·기아 자동차 관련 자주 묻는 질문(FAQ)을 웹 크롤링하여 DB에 저장하고, 키워드 검색 및 카테고리별 조회 기능 제공 |



### ERD

<img width="500" height="239" alt="Image" src="https://github.com/user-attachments/assets/a07440b5-0512-4731-b00a-2edc019446d2" />

### 수행결과(시연 페이지)

### 한 줄 회고

- 양정민 : 정신없이 빠르게 지나간 시간 만큼이나 진행을 따라가기 어려웠다만 팀원들이 잘해주시고 챙겨주셔서 그래도 마음 편하게 임하여 그나마 streamlit은 어느정도 감이 잡힌거 같습니다.
  
- 조해리 : 기업별 faq의 경우 더 다양한 기업의 faq를 가져올 수 있었으면 더 좋았을 것 같다. 주제 구체화에 많은 시간이 소모되어 자료 수집을 비교적 많이 하지 못한 것이 매우 아쉬웠다. 그리고 streamlit 코드 작성을 하다보니 반복적으로 들어가는 부분이 많아졌는데, 코드를 다시 살펴보고 정리하지 않은 것 또한 아쉬운 부분이다.

- 김준협 :


- 이재은 : ERD 설계 과정에서 여러 차례 시행착오를 겪으며 데이터 모델링 방법을 명확히 이해하게 되었다. 현대 FAQ 크롤링을 진행하면서 텍스트가 제대로 추출되지 않는 문제를 경험했지만, 이를 해결하며 문제 해결 능력이 크게 향상되었다. 이런 과정을 통해 예기치 않은 오류들을 직접 다뤄보면서 기술적 성장과 실전 감각을 키울 수 있었다.
