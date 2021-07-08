import os.path
import json
import api
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from decouple import config
from datetime import date

def updateFacebookCustomAudience(SPREADSHEET_ID,spreadsheet,adAccountId):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = config('PATH_TO_SERVICE_JSON')

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=spreadsheet).execute()
    values = result.get('values', [])

    rawDate = date.today()
    today = rawDate.strftime("%d/%m/%Y")

    if values[0][len(values[0])-1] != today:
        print("Updating")

        api.getCustomAudiences(adAccountId)
        CustomAudiences = open(os.getcwd() + '/stored_data/' + str(adAccountId) + '_custom_audiences.json')
        CustomAudiences = json.load(CustomAudiences)

        for x in range(len(values)):
            line = values[x]

            if x == 0:
                line.append(today)
                pass

            else:
                updatedNames = []
                for i in range(len(CustomAudiences['data'])):
                    name = CustomAudiences['data'][i]['name']
                    size = CustomAudiences['data'][i]['approximate_count']
                    if line[0] == name and name not in updatedNames:
                        line.append(size)
                        updatedNames.append(name)
                    pass
                pass
        pass
    else:
        print("Spreadsheets are updated")

    request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
    range=spreadsheet,valueInputOption="USER_ENTERED", body={"values":values})
    response = request.execute()

    print(response['updatedCells'])
    pass