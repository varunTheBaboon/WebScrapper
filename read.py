
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account




SERVICE_ACCOUNT_FILE = 'keys.json'
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)






# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1r9uRW8T74x-hrURdwiNH-gqvZZRZyosei0o4jj4B-Os'




service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="A1:G13").execute()
values = result.get('values', [])
aoa = [{"Cost":39}]
request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A1", valueInputOption="USER_ENTERED",body={"values":aoa})
response = request.execute()
if not values:
    print('No data found.')
else:
    print(result)


