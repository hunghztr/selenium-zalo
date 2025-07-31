from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from open_zalo import open_zalo
from data_from_sheet import get_data_from_sheet
from selenium.webdriver.common.keys import Keys
import re
# *
# LƯU Ý KHI CHẠY TOOL CẦN THU NỬA MÀN HÌNH ĐỂ CODE KHÔNG LỖI
# *
def remove_non_bmp_chars(text):
    # Chỉ giữ lại: chữ cái Latin + tiếng Việt có dấu + số + dấu câu + khoảng trắng
    pattern = r"[^a-zA-Z0-9ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯàáâầậãèéêếểệễìíòóôổộõùúăđĩũơớợởưửẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀẾỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸỳỵỷỹ\s.,:;!?+-]"
    text = re.sub(pattern, ' ', text)

    # Loại bỏ các ký tự ngoài BMP (như emoji, chữ Trung-Nhật-Hàn,...)
    text = re.sub(r'[^\u0000-\uFFFF]', ' ', text)

    # Gộp khoảng trắng liên tiếp thành 1
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def send_message(content):
    try:
        contents = content.split("\n")
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'input_line_0')))
        input_box = driver.find_element(By.ID, "input_line_0")
        input_box.click()
        for c in contents:
            input_box = driver.find_element(By.ID, "input_line_0")
            input_box.send_keys(c)
            input_box.send_keys(Keys.SHIFT, Keys.ENTER)
          
        time.sleep(0.5)
        input_box = driver.find_element(By.ID, "input_line_0")
        input_box.send_keys(Keys.ENTER)
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Không tìm thấy ô nhập tin nhắn: {e}")
        return False
    time.sleep(0.5)
    return True
def send_message_to_group():
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'contact-search-input')))
    search_box = driver.find_element(By.ID, "contact-search-input")
    values = get_data_from_sheet()
    sended = list()
    finished = 0
    for value in values:
        search_box.click()
        print("Đã click vào ô tìm kiếm")
        stt = value[0] if len(value) > 0 else ""
        group_name_from_sheet = value[1] if len(value) > 1 else ""
        members = value[2] if len(value) > 2 else ""
        content = value[3] if len(value) > 3 else ""
        print(f"STT: {stt} | GROUP NAME: {group_name_from_sheet} | MEMBERS: {members} | CONTENT: {content}")
        group_name_from_sheet = remove_non_bmp_chars(group_name_from_sheet)
        time.sleep(0.5)
        # kiểm tra nhóm này trùng tên với nhóm đã gửi hay không
        if group_name_from_sheet in sended:
            count = sended.count(group_name_from_sheet)
            search_box.send_keys(group_name_from_sheet)
            time.sleep(0.5)
            # lấy ra danh sách kết quả tìm kiếm
            group_items = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'group-item-')]")
            time.sleep(0.5)
            group_items[count].click()
        else:
            search_box.send_keys(group_name_from_sheet)
            time.sleep(0.5)
            # lấy ra danh sách kết quả tìm kiếm
            group_items = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'group-item-')]")
            for item in group_items:
                time.sleep(0.5)
                name_element = item.find_element(By.CLASS_NAME, "truncate")
                time.sleep(0.5)
                name_from_result = remove_non_bmp_chars(name_element.text.split("\n")[0])
                print(f"Tên nhóm tìm kiếm: {name_from_result}")
                if name_from_result in group_name_from_sheet:
                    item.click()
                    print(f"Đã click vào nhóm: {name_from_result}")
                    break
        sended.append(group_name_from_sheet)
        time.sleep(0.5)
        isSuccess = send_message(content)
        if isSuccess:
            finished += 1
            print(f"Đã gửi tin nhắn đến nhóm: {group_name_from_sheet}")
        else:
            print(f"Không gửi được tin nhắn đến nhóm: {group_name_from_sheet}")
        # bấm nút back để quay lại danh sách nhóm
        try:
            back_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'conv-back-btn')]")
        except Exception as e:
            print(f"Không tìm thấy nút back: {e}")
        time.sleep(0.5)
        back_btn.click()
    print(f"✅ Đã gửi tin nhắn đến {finished} nhóm")
driver,wait = open_zalo()

send_message_to_group()

driver.quit()