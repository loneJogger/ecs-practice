# import statements
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import settings

# gets email addresses of current Lit Hold users.
def getLitHoldEmails():

    secret = os.path.join(os.getcwd(), 'googs.json')
    creds = service_account.Credentials.from_service_account_file(secret, scopes=settings.SCOPES, subject=settings.SUBJECT)


    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=settings.SPREADSHEET_ID, range=settings.RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('no values found...')
        return set(['no values!'])
    else:
        res = set([])
        for cell in values:
            if len(cell) > 0:
                res.add(cell[0].lower())
        return res
