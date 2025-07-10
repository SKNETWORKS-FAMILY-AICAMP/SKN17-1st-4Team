from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

path = 'chromedriver.exe'
service = webdriver.chrome.service.Service(path)
driver = webdriver.Chrome(service=service)

driver.get("https://www.kia.com/kr/customer-service/center/faq")
time.sleep(1)

# 차량정비 탭 이동
kia_btn = driver.find_element(By.XPATH, '//*[@id="tab-list"]/li[4]/button')
kia_btn.click()
time.sleep(1)

# 데이터 가져오기
data = []

def data_kia():
    # for i in range(10):
    #     item = driver.find_element(By.ID, f"accordion-item-{i}")
    #     #질문
    #     question_elem = item.find_element(By.CSS_SELECTOR, "span.cmp-accordion__title")
    #     question = question_elem.text
    #     #답변
    #     button = item.find_element(By.CSS_SELECTOR, "button.cmp-accordion__button")
    #     #버튼 열기
    #     if button.get_attribute("aria-expanded") == "false":
    #         button.click()
    #         time.sleep(1)
    #     answer_elem = item.find_elements(By.CSS_SELECTOR, "div.faqinner__wrap p")
    #     answer = ''.join(p.text for p in answer_elem)

    #     data.append({"질문": question, "답변": answer})
    items = driver.find_elements(By.CSS_SELECTOR, 'div.cmp-accordion__item')
    for item in items:
        # 질문
        question = item.find_element(By.CSS_SELECTOR, "span.cmp-accordion__title").text
        # 답변
        button = item.find_element(By.CSS_SELECTOR, "button.cmp-accordion__button")
        if button.get_attribute("aria-expanded") == "false":
            button.click()
            time.sleep(0.5)
        answer_elems = item.find_elements(By.CSS_SELECTOR, "div.faqinner__wrap p")
        #answer = ''.join(p.text for p in answer_elems)
        answer = ' '.join(p.text.strip() for p in answer_elems)
        data.append({"질문": question, "답변": answer})

# 페이지 이동
def pages():
    for i in range(4):
        next_page = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div[3]/div/div/div[4]/div/ul/li[{i+2}]')
        next_page.click()
        time.sleep(1)
        data_kia()
        time.sleep(3)

# 탭 이동
def tabs():
    next_tab = driver.find_element(By.XPATH,'//*[@id="contents"]/div/div[3]/div/div/div[4]/div/button')

    next_tab.click()
    time.sleep(3)
    data_kia()
    time.sleep(2)

def tabs_2():
    next_tab = driver.find_element(By.XPATH,'//*[@id="contents"]/div/div[3]/div/div/div[4]/div/button[2]')

    next_tab.click()
    time.sleep(3)
    data_kia()
    time.sleep(2)

#-1페이지
data_kia()

#-2~16페이지
# for t in range(3):
#     pages()
#     tabs()

#-2~6페이지
pages()
tabs()

#-7~10페이지
pages()
#-11페이지
tabs_2()
#-12~15페이지
pages()
#-16페이지
tabs_2()

#print(data)
df = pd.DataFrame(data)

df = pd.DataFrame(data)
print("전체 수집 개수:", len(df))

# 질문만 중복 제거
df_question_unique = df.drop_duplicates(subset=["질문"])
print("질문 기준 중복 제거:", len(df_question_unique))

# 질문+답변 모두 중복 제거
df_full_unique = df.drop_duplicates(subset=["질문", "답변"])
print("질문+답변 기준 중복 제거:", len(df_full_unique))
df.to_csv('kia_faq.csv', index=False, encoding='utf-8-sig')
print('@@@CSV 저장 완료!@@@')
driver.quit()