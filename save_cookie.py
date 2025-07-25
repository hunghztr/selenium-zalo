
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import sys
import subprocess
try:
    # Khởi động Chrome với remote debugging
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    debug_port = "--remote-debugging-port=9222"
    user_data_dir = r'--user-data-dir=C:/Chrome_dev'
    # Mở Chrome với remote debugging
    subprocess.Popen([chrome_path, debug_port, user_data_dir])
    time.sleep(2)  # Thời gian chờ để Chrome khởi động
    # Thiết lập Chrome Options để kết nối tới phiên Chrome đang mở
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # Kết nối tới Chrome đang mở
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)
    print("Đang mở trang web...")
    driver.execute_script("window.open('https://chat.zalo.me/', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10)  # Chờ thêm để trang tải đầy đủ

except Exception as e:
    print(f"Lỗi khi mở trang web: {e}")
    driver.quit()
    sys.exit()
# Chờ tối đa 30 giây cho đến khi phần tử có ID 'contact-search-input' xuất hiện
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'contact-search-input')))
# Tìm và lưu trữ phần tử có id 'contact-search-input' bằng cách sử dụng cú pháp XPath
sels = driver.find_element(By.XPATH, "//input[@id='contact-search-input']")
# In ra giá trị của biến 'sels' để kiểm tra xem phần tử đã được tìm thấy
print("sels", sels)