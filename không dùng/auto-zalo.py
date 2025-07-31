import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException, NoSuchElementException
import time

browser = webdriver.Firefox()

browser.get('https://chat.zalo.me')
time.sleep(180)  
clicked_links = set()  

def get_contact():
    try:
        contact_icon = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]/div[1]/i'))
        )
        contact_icon.click()
        
        community_list = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/nav/div[2]/div[3]/div/div[2]'))
        )
        community_list.click()
        
        group_to_chat = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div[2]/div/div[1]/div/div[1]/div/div/div[4]/div/div[1]'))
        )
        group_to_chat.click()
    except (ElementClickInterceptedException, TimeoutException) as e:
        print(f"Lỗi khi click vào phần tử mong muốn...")

def find_and_click_latest_link():
    try:
        messages = browser.find_elements(By.CLASS_NAME, 'overflow-hidden')
        
        for message in reversed(messages):
            if 'https://zalo.me' in message.text:
                try:
                    link = message.find_element(By.TAG_NAME, 'a')
                    link_content = link.get_attribute('content')  
                    if link_content not in clicked_links:
                        clicked_links.add(link_content)
                        print(f"Nhấn vào liên kết: {link_content}")

                        try:
                            link.click()
                        except ElementClickInterceptedException:
                            print("Click vào liên kết.")
                            browser.execute_script("arguments[0].click();", link)

                        time.sleep(5)  

                        try:
                            join_button = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[2]/div'))
                            )
                            join_button.click()
                            time.sleep(2)  
                        except (TimeoutException, NoSuchElementException):
                            print("Không tìm thấy nút 'Tham gia', tiếp tục...")

                        try:
                            click_to_cancel = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div[2]/i'))
                            )
                            click_to_cancel.click()
                            print("Nhấn vào nút hủy thành công.")
                        except (TimeoutException, NoSuchElementException):
                            print("Không tìm thấy nút hủy, tiếp tục...")

                        return  
                except NoSuchElementException:
                    continue  

    except StaleElementReferenceException:
        print("Không tìm thấy phần tử, bỏ qua và thử lại sau.")


while True:
    get_contact()
    time.sleep(10)
    find_and_click_latest_link()
