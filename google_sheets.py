from pprint import pprint

from dotenv import load_dotenv
import os

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

from CONSTANTS import CREDENTIALS_FILE

load_dotenv()

GOOGLE_SHEET_ID = os.getenv("SPREADSHEET_ID")

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
http_auth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=http_auth)


def fill_whole_table(data):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=GOOGLE_SHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"Sheet1!A9:C{9 + len(data)}",
                 "majorDimension": "ROWS",
                 "values": data}
            ]
        }).execute()

    pprint(values)
