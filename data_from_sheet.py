import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_auth():
   # Xác thực
    creds = service_account.Credentials.from_service_account_file('hellojobv5-8406e0a8eed7.json')
    service = build('sheets', 'v4', credentials=creds)

    # Thông tin bảng
    spreadsheet_id = '1ccRbwgDPelMZmJlZSKtxbWweZ9UsgvgYjkpvMX1x1TI'
    sheet_name = 'nhóm trong zalo'
    return service, spreadsheet_id, sheet_name

def get_data_from_sheet():
  service, spreadsheet_id, sheet_name = get_auth()
# Lấy dữ liệu từ cột A và B, bắt đầu từ dòng 2
  range_name = f'{sheet_name}!A2:B'
  result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
  values = result.get('values', [])
  return values

def append_stt_and_name(name):
    service, spreadsheet_id, sheet_name = get_auth()

    # Lấy dữ liệu từ cột A để tìm STT cuối cùng
    range_check = f'{sheet_name}!A1:A'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_check).execute()
    existing_rows = result.get('values', [])

    # Tính STT tiếp theo
    if not existing_rows:
        # Nếu không có dữ liệu, bắt đầu từ 1
        next_stt = 1
    else:
        next_stt = len(existing_rows) + 1

    # Ghi dữ liệu mới (STT, Tên) vào cuối bảng
    range_append = f'{sheet_name}!A:B'
    values = [[next_stt, name]]  # STT + tên
    body = {
        'values': values
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_append,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

    print(f"Đã thêm STT {next_stt} | Tên: {name}")
