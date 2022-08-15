from pprint import pprint

from dotenv import load_dotenv
import os

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

from CONSTANTS import CREDENTIALS_FILE
from handlers import make_total_data_array

load_dotenv()

GOOGLE_SHEET_ID = os.getenv("SPREADSHEET_ID")

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
http_auth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=http_auth)


def fill_whole_table(data):
    # print(data)
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=GOOGLE_SHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"A9:N{8 + len(data)}",
                 "majorDimension": "ROWS",
                 "values": data}
            ]
        }).execute()

    # pprint(values)


def start_spreadsheet():
    user_data = service.spreadsheets().values().get(
        spreadsheetId=GOOGLE_SHEET_ID,
        majorDimension="ROWS",
        range="B4:B6"
    ).execute()["values"][0]

    try:
        bank_amount = float(user_data[0])
    except Exception:
        bank_amount = 0.0
    try:
        buy_limit = float(user_data[1])
    except Exception:
        buy_limit = 0
    try:
        sell_limit = float(user_data[2])
    except Exception:
        sell_limit = 0

    fill_whole_table(make_total_data_array("RUB", bank_amount, {"BUY": buy_limit,
                                                                "SELL": sell_limit}))
