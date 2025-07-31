import sys
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException, NoSuchElementException
import time
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from openaitool import analyzeAndSplitJobContent, analyzeJobInformation

import rapidjson

browser = webdriver.Firefox()
browser.get('https://chat.zalo.me')
time.sleep(30)

unique_messages = set()
messages_data = []
i = 0
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SPREADSHEET_ID = '1tKFLe2taCc9AhpvsrLT9ySGwMJDPCo1QxS3YcnvyJmE'  sheet cũ
SPREADSHEET_ID = '1ccRbwgDPelMZmJlZSKtxbWweZ9UsgvgYjkpvMX1x1TI'


def authenticate_google_sheets():
    credentials = Credentials.from_service_account_file(
        "hellojobv5-bbd1a88506df.json", scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service


def get_contact():
    try:
        print(f"Bắt đầu tìm kiếm và chọn nhóm")
        contact_icon = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'fa.fa-Contact_28_Line.internal-icon'))
        )
        contact_icon.click()

        community_list = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'fa.fa-Community_List_24_Line.menu__icon'))
        )
        community_list.click()

        group_to_chat = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'friend-info'))
        )
        group_to_chat.click()
    except (ElementClickInterceptedException, TimeoutException) as e:
        print(f"Lỗi khi click vào phần tử mong muốn.")
        return


def fetch_message_zalo():
    service = authenticate_google_sheets()
    global unique_messages, messages_data, i
    try:
        chatItems = browser.find_elements(By.CLASS_NAME, 'chat-item')
        threadChatTitle = browser.find_element(
            By.CLASS_NAME, 'threadChat__title')
        groupName = threadChatTitle.text.replace('&nbsp;', ' ')
        global lastSenderName
        rowInserted=1
        for chatItem in chatItems:
            try:
                sender = chatItem.find_element(
                    By.CLASS_NAME, 'card-sender-name')
                lastSenderName = sender.text
            except NoSuchElementException:
                pass
            messages = chatItem.find_elements(
                By.CSS_SELECTOR, '[data-component="message-text-content"]')
            if messages:
                message = messages[0]
                message_text = message.text
                if message_text and message_text not in unique_messages:
                    unique_messages.add(message_text)
                    analyzeJobContent = analyzeAndSplitJobContent(
                        groupName, message_text)
                    analyzeJobContentUsage = analyzeJobContent.usage
                    choiceJsonStr = analyzeJobContent.choices[0].message.content
                    count = 0
                    try:
                        if not choiceJsonStr:
                            decodedJobs = [choiceJsonStr]
                        else:
                            decodedJobs = rapidjson.loads(choiceJsonStr)
                    except Exception:
                        decodedJobs = [choiceJsonStr]
                        pass
                    for job in decodedJobs:
                        if len(job) >= 10:
                            analyzeJobInfo = analyzeJobInformation(
                                groupName, lastSenderName, job)
                            prompt_tokens = 0
                            completion_tokens = 0
                            if count == 0:
                                prompt_tokens = analyzeJobContentUsage.prompt_tokens
                                completion_tokens = analyzeJobContentUsage.completion_tokens
                                count += 1
                            jobInforString = analyzeJobInfo.choices[0].message.content
                            analyzeJobInfoUsage = analyzeJobInfo.usage
                            prompt_tokens += analyzeJobInfoUsage.prompt_tokens
                            completion_tokens += analyzeJobInfoUsage.completion_tokens
                            prompt_price = round(
                                prompt_tokens * 2.5 / 1000000, 4)
                            completion_price = round(
                                completion_tokens*10 / 1000000, 4)
                            new_row = [groupName, lastSenderName,
                                       job, jobInforString]
                            try:
                                jobInfor = rapidjson.loads(jobInforString)
                                if groupName.find('Tokutei Việt 🇻🇳 - Team Phương'):
                                    jobInfor.visa='Tokutei đầu Việt'
                                elif groupName.find('Tokutei Nhật - Team Phương'):
                                    jobInfor.visa='Tokutei đầu Nhật'
                                new_row += formatJob(jobInfor)
                                new_row += [prompt_tokens, completion_tokens,
                                            prompt_price, completion_price]
                            except Exception:
                                pass
                            new_row.insert(0, int(time.time()))
                            new_row.insert(0, '0')
                            append_row_to_google_sheet(service, new_row)
                            print(f'============')
                            print(f'Đã phân tích '+str(len(unique_messages))+' tin')
                            print(f'Đã insert được '+str(rowInserted)+' dòng')
                            rowInserted+=1
                    if len(unique_messages) >= 200:
                        # save_to_excel(messages_data)
                        unique_messages.clear()
                        sys.exit()

    except Exception:
        print("Không tìm thấy đoạn chat, đang thử lại.....")
        pass


def append_row_to_google_sheet(service, values):
    sheet = service.spreadsheets()
    body = {
        'values': [values]  # Danh sách dữ liệu cho một dòng
    }
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='DonHang!A1',  # Ghi dữ liệu vào Sheet1, bắt đầu từ A1
        valueInputOption='RAW',
        body=body
    ).execute()
    print(f"Đã ghi thành công: {result.get('updates').get('updatedCells')} ô.")


def save_to_excel(data):
    global i
    df = pd.DataFrame(data)
    real_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    i += 1
    filename = f"{real_time}messages{i}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Lấy dữ liệu lần {i}")


def formatJob(data):
    fields = [
        "contact", "country", "visa", "career", "workLocation",
        "interviewFormat", "language", "languageLevel", "fee",
        "back", "quantity", "basicSalary", "realSalary", "minAge",
        "maxAge", "gender", "interviewDay", "height", "weight",
        "dominantHand", "requiredQualifications", "numberRecruits",
        "haveTattoo", "vgb", "specialConditions"
    ]
    result = []
    for field in fields:
        # Use .get() to avoid KeyError if the field is missing in the data object
        value=data.get(field, 'Empty')
        if value=='' or value=='Empty':
            value='Không rõ'
        result.append(value)
    return result


# get_contact()
# time.sleep(10)
print(f"Bắt đầu thu thập dữ liệu........")
count = 50
while True:
    fetch_message_zalo()
    count = count+1
    time.sleep(5)
    # if count >= 10:
    #     break
