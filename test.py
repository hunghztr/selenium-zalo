from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def scroll_and_click_groups(browser, interval=20):
    try:
        groups = browser.find_elements(By.XPATH, "//div[contains(@class, 'msg-item')]")
        print(f"Tổng số nhóm: {len(groups)}")
        for group in groups:
            group.click()
            print("Đã click vào nhóm ", group.text)
            time.sleep(5)
    except Exception as e:
        print(f"loi",e)
# Setup Chrome
driver_path = "C:/chromedriver/chromedriver.exe"
options = Options()
options.add_argument("--start-maximized")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 1. Mở Zalo Web
driver.get("https://chat.zalo.me")
time.sleep(30)  # Thời gian để bạn đăng nhập thủ công
scroll_and_click_groups(driver)

# Đóng trình duyệt
driver.quit()
