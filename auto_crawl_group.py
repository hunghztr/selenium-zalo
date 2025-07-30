from open_zalo import open_zalo
from data_from_sheet import append_stt_and_name
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys


driver, wait = open_zalo()
# WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'mmi-icon-wr')))
contact_btn = driver.find_element(By.XPATH, "//div[@title='Danh bạ']")
contact_btn.click()
print("Đã click vào nút liên hệ")
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

# Vừa cuộn vừa lấy tên
for i in range(15):  # Số lần cuộn (tùy chỉnh)
    time.sleep(0.5)
    # Tìm các thẻ span tên nhóm đang hiển thị
    # Tìm phần tử mới trong từng vòng lặp
    name_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "contact-item-v2-wrapper")]//span[contains(@class, "name")]')
    for i in range(len(name_elements)):
        try:
        # Luôn lấy lại phần tử mới sau mỗi vòng cuộn
          name_element = driver.find_elements(By.XPATH, '//div[contains(@class, "contact-item-v2-wrapper")]//span[contains(@class, "name")]')[i]
          name = name_element.text
          if name and name not in collected_names:
              collected_names.add(name)
              print("➕ Nhóm:", name)
              append_stt_and_name(name)
        except Exception as e:
          print(f"Lỗi khi lấy tên nhóm: {e}")

    scroll_container.send_keys(Keys.PAGE_DOWN)
    print(f"Đã cuộn {i+1} lần")
print(f"✅ Tổng số nhóm đã thu thập: {len(collected_names)}")
input("Nhấn Enter để kết thúc...")

