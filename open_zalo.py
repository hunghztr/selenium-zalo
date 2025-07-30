import sys
import subprocess
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def open_zalo():
  try:
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    debug_port = "--remote-debugging-port=9222"
    user_data_dir = r'--user-data-dir=C:/Chrome_dev'
    subprocess.Popen([chrome_path, debug_port, user_data_dir])
    time.sleep(2)  # Thời gian chờ để Chrome khởi động
    # Thiết lập Chrome Options để kết nối tới phiên Chrome đang mở
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # ➕ Thêm tùy chọn kích thước và vị trí cửa sổ (nửa màn hình bên phải)
    chrome_options.add_argument("--window-size=960,1080")
    chrome_options.add_argument("--window-position=960,0")

    # Kết nối tới Chrome đang mở
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 30)
    print("Đang mở trang web...")
    driver.execute_script("window.open('https://chat.zalo.me/', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)  # Chờ thêm để trang tải đầy đủ
    return driver,wait
  except Exception as e:
    print(f"Lỗi khi mở trang web: {e}")
    driver.quit()
    sys.exit()