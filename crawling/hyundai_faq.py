from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. 크롬 브라우저 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# 2. 현대차 FAQ 페이지 접속
driver.get("https://www.hyundai.com/kr/ko/e/customer/center/faq")
time.sleep(2)

# 3. 스크롤 2번 (탭 클릭 전)
for _ in range(2):
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)

# 4. 차량정비 탭 클릭
car_tab_xpath = '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[1]/div[1]/ul/li[2]/button/span'
car_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, car_tab_xpath))
)
driver.execute_script("arguments[0].click();", car_tab)
time.sleep(2)

def scrape_page(page_num):
    print(f"\n===== Page {page_num} =====")
    for i in range(1, 11):
        try:
            question_xpath = f'//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[1]/div[{i}]/button/div/span[2]'
            question_elem = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, question_xpath))
            )
            question_text = question_elem.get_attribute("innerText").strip()

            click_btn_xpath = f'//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[1]/div[{i}]/button'
            click_btn = driver.find_element(By.XPATH, click_btn_xpath)

            # Q1, Q2만 스크롤
            if i in [1, 2]:
                driver.execute_script("arguments[0].scrollIntoView(true);", question_elem)
                time.sleep(0.5)

            driver.execute_script("arguments[0].click();", click_btn)
            time.sleep(0.5)

            # Q1 답변 후 스크롤 1번
            if i == 1:
                driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(1)

            # 전체 답변 수집
            answer_container_xpath = f'//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[1]/div[{i}]/div/div'
            answer_container = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, answer_container_xpath))
            )
            full_answer = answer_container.text.strip()

            print(f"Q{i}. {question_text}")
            print(f"A{i}. {full_answer}\n")

        except Exception as e:
            print(f"[오류] Q{i} (page {page_num}): {e}")

    # 마지막 질문까지 뽑은 후 스크롤
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)

# ✅ 1~4페이지 수집
scrape_page(1)

page_buttons_2_4 = [
    '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/div/ul/li[2]/button',
    '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/div/ul/li[3]/button',
    '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/div/ul/li[4]/button'
]

for idx, btn_xpath in enumerate(page_buttons_2_4, start=2):
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, btn_xpath))
        )
        btn.click()
        time.sleep(2)
        scrape_page(idx)
    except Exception as e:
        print(f"[페이지 이동 실패] page {idx}: {e}")
        break

# ✅ ▶️ 화살표 클릭 후 5~8페이지 수집
try:
    next_arrow_xpath = '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/button[3]'
    next_arrow = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, next_arrow_xpath))
    )
    next_arrow.click()
    time.sleep(2)
except Exception as e:
    print(f"[다음 화살표 클릭 실패]: {e}")

page_buttons_5_8 = [
    '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/div/ul/li[1]/button',
    '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/div/ul/li[2]/button',
    '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/div/ul/li[3]/button',
    '//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[3]/div[2]/div/ul/li[4]/button'
]

for idx, btn_xpath in enumerate(page_buttons_5_8, start=5):
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, btn_xpath))
        )
        btn.click()
        time.sleep(2)
        scrape_page(idx)
    except Exception as e:
        print(f"[페이지 이동 실패] page {idx}: {e}")
        break

# 브라우저 종료
driver.quit()







