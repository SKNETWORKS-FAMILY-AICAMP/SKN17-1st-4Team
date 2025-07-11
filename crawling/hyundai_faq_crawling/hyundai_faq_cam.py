from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 1. 크롬 브라우저 실행
path = 'chromedriver.exe'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)

# 2. 현대차 FAQ 페이지 접속
driver.get("https://www.hyundai.com/kr/ko/e/customer/center/faq")
time.sleep(2)

# 3. 빌트인캠 탭 클릭
hcar_buy_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[1]/div[1]/ul/li[8]/button')
hcar_buy_btn.click()
time.sleep(2)

# 데이터 수집
data = []
def hcar_data():
    items = driver.find_elements(By.CSS_SELECTOR, 'div.list-item')
    for item in items:
        # 질문
        question = item.find_element(By.CSS_SELECTOR,'span.list-content').text.strip()
        #print(question)
        # 답변
        button = item.find_element(By.CSS_SELECTOR, 'button.list-title')
        #button.click()
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        answer_elems = item.find_elements(By.CSS_SELECTOR, "div.conts")
        #answer = ' '.join(a.text.strip() for a in answer_elems)
        answer = ' '.join(a.text.strip().replace('\n', ' ') for a in answer_elems)

        data.append({"질문": question, "답변": answer})

# 4. 페이지 이동 및 데이터 수집 (빌트인캠 1페이지)
# def pages():
#     for i in range(3):
#         next_page = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/button[3]')
#         next_page.click()
#         time.sleep(2)
#         hcar_data()

hcar_data()
#pages()
#print(data)

df = pd.DataFrame(data)
print("전체 수집 개수:", len(df))

df.to_csv('hyundai_faq_cam.csv', index=False, encoding='utf-8-sig')
print('@@@CSV 저장 완료!@@@')

# 브라우저 종료
driver.quit()