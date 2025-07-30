
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from open_zalo import open_zalo
from data_from_sheet import get_data_from_sheet
def scroll_and_click_groups(browser, interval=20):
    try:
       
        groups = browser.find_elements(By.XPATH, "//div[contains(@class, 'msg-item')]")
        print(f"Tổng số nhóm: {len(groups)}")
        for group in groups:
            group.click()
            print("Đã click vào nhóm ", group.text)
            time.sleep(5)
            # Chờ khung nhập tin nhắn xuất hiện
            input_box = wait.until(EC.presence_of_element_located((By.ID, "input_line_0")))

            # Nhập nội dung tin nhắn
            input_box.click()
            input_box.send_keys("hello")
            time.sleep(1)
                # Gửi tin nhắn bằng cách ấn Enter
            input_box.send_keys("\n")

            print("Đã gửi tin nhắn")
    except Exception as e:
        print(f"loi",e)
def send_message():
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'input_line_0')))
    input_box = driver.find_element(By.ID, "input_line_0")
    input_box.click()
    input_box.send_keys("hello")
    time.sleep(1)
    input_box.send_keys("\n")
    time.sleep(1)
def send_message_to_group():
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'contact-search-input')))
    search_box = driver.find_element(By.ID, "contact-search-input")
    values = get_data_from_sheet()

    for value in values:
        search_box.click()
        print("Đã click vào ô tìm kiếm")
        a = value[0] if len(value) > 0 else ""
        b = value[1] if len(value) > 1 else ""
        print(f"A: {a} | B: {b}")
        search_box.send_keys(b)
        time.sleep(2)
        search_box.send_keys("\n")
        time.sleep(2)
        send_message()
        print(f"Đã gửi tin nhắn đến nhóm: {b}")
driver,wait = open_zalo()

send_message_to_group()


input("Nhấn Enter để đóng trình duyệt...")
driver.quit()