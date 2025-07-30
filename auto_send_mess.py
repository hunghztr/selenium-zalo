
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from open_zalo import open_zalo
from data_from_sheet import get_data_from_sheet
from selenium.webdriver.common.keys import Keys
import re

def remove_non_bmp_chars(text):
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

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
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'input_line_0')))
        input_box = driver.find_element(By.ID, "input_line_0")
        input_box.click()
        input_box.send_keys("hello")
        time.sleep(1)
        input_box.send_keys("\n")
    except Exception as e:
        print(f"Không tìm thấy ô nhập tin nhắn: {e}")
    time.sleep(1)
def send_message_to_group():
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'contact-search-input')))
    search_box = driver.find_element(By.ID, "contact-search-input")
    values = get_data_from_sheet()
    sended = list()
    for value in values:
        search_box.click()
        print("Đã click vào ô tìm kiếm")
        stt = value[0] if len(value) > 0 else ""
        group_name = value[1] if len(value) > 1 else ""
        members = value[2] if len(value) > 2 else ""
        print(f"STT: {stt} | GROUP NAME: {group_name} | MEMBERS: {members}")
        group_name = remove_non_bmp_chars(group_name)
        time.sleep(0.5)
        # kiểm tra nhóm này trùng tên với nhóm đa gửi hay không
        if group_name in sended:
            count = sended.count(group_name)
            search_box.send_keys(group_name)
            time.sleep(0.5)
            # lấy ra danh sách kết quả tìm kiếm
            group_items = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'group-item-')]")
            time.sleep(0.5)
            group_items[count].click()
        else:
            search_box.send_keys(group_name)
            time.sleep(0.5)
            # lấy ra danh sách kết quả tìm kiếm
            group_items = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'group-item-')]")
            for item in group_items:
                time.sleep(0.5)
                name_element = item.find_element(By.CLASS_NAME, "truncate")
                time.sleep(0.5)
                # spans = name_element.find_elements(By.CLASS_NAME, "txt-highlight")
                # print(f"Số lượng phần tử tìm thấy: {len(spans)}")
                # for span in spans:
                #     print(f"Span text: {span.text}")
                # name = "".join(span.text + " " for span in spans).strip()
                name = name_element.text.split("\n")[0]
                print(f"Tên nhóm tìm kiếm: {name}")
                if name in group_name:
                    item.click()
                    print(f"Đã click vào nhóm: {name}")
                    break
        sended.append(group_name)
        time.sleep(0.5)
        send_message()
        print(f"Đã gửi tin nhắn đến nhóm: {group_name}")
        # bấm nút back để quay lại danh sách nhóm
        back_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'conv-back-btn')]")
        time.sleep(0.5)
        back_btn.click()
driver,wait = open_zalo()

send_message_to_group()


input("Nhấn Enter để đóng trình duyệt...")
driver.quit()