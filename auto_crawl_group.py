from open_zalo import open_zalo
from data_from_sheet import append_stt_and_name
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

# *
# LƯU Ý KHI CHẠY TOOL CẦN THU NỬA MÀN HÌNH ĐỂ CODE KHÔNG LỖI
# *
driver, wait = open_zalo()
# WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'mmi-icon-wr')))
contact_btn = driver.find_element(By.XPATH, "//div[@title='Danh bạ']")
contact_btn.click()
print("Đã click vào nút liên hệ")
time.sleep(0.5)
try:
    back_btn = driver.find_element(By.XPATH, "//div[contains(@class, 'conv-back-btn')]")
except Exception as e:
    print(f"Không tìm thấy nút back: {e}")
back_btn.click()
time.sleep(0.5)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.menu-item.flx.middle-flex.clickable')))
group_btns = driver.find_elements(By.CSS_SELECTOR, "div.menu-item.flx.middle-flex.clickable")
group_btns[1].click()
print("Đã click vào nút nhóm")
time.sleep(0.5)
# Tìm khung cuộn danh sách hội nhóm
scroll_container = driver.find_element(
    By.CSS_SELECTOR,
    "div.ReactVirtualized__Grid.ReactVirtualized__List.contact-tab-v2__list-custom"
)

collected_names = set()

scroll_attempts = 0
max_attempts = 50  # Giới hạn cuộn tối đa để tránh vòng lặp vô tận
previous_count = 0

while scroll_attempts < max_attempts:
    time.sleep(0.5)
    name_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "contact-item-v2-wrapper")]//span[contains(@class, "name")]')
    
    for i in range(len(name_elements)):
        try:
            name_element = driver.find_elements(By.XPATH, '//div[contains(@class, "contact-item-v2-wrapper")]//span[contains(@class, "name")]')[i]
            name = name_element.text
            parent = name_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'contact-item-v2-wrapper')]")
            try:
                member_element = parent.find_element(By.CSS_SELECTOR, "a.description.left.members")
                member = member_element.text
            except:
                member = "Không tìm thấy số thành viên"
            if name and member:
                group = (name, member)
                if group not in collected_names:
                    collected_names.add(group)
                    print("➕ Nhóm:", name," Số thành viên:", member)
                    append_stt_and_name(group)
        except Exception as e:
            print(f"Lỗi khi lấy tên nhóm: {e}")
    
    # So sánh số lượng nhóm trước và sau cuộn
    current_count = len(collected_names)
    if current_count == previous_count:
        print("🚫 Không có nhóm mới. Dừng cuộn.")
        break
    previous_count = current_count

    scroll_container.send_keys(Keys.PAGE_DOWN)
    scroll_attempts += 1
    print(f"⬇️ Đã cuộn {scroll_attempts} lần")
print(f"✅ Tổng số nhóm đã thu thập: {len(collected_names)}")
driver.quit()

