import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_data_from_sheet():
  creds = service_account.Credentials.from_service_account_file('hellojobv5-8406e0a8eed7.json')
  service = build('sheets', 'v4', credentials=creds)

# Thông tin bảng và phạm vi
  spreadsheet_id = '1ccRbwgDPelMZmJlZSKtxbWweZ9UsgvgYjkpvMX1x1TI'
  sheet_name = 'Test tool zalo hùng'

# Lấy dữ liệu từ cột A và B, bắt đầu từ dòng 2
  range_name = f'{sheet_name}!A2:B'
  result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
  values = result.get('values', [])
  return values

