from calendar import calendar
import datetime
from math import remainder
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_service(client_secrect_file, scopes):
    CLIENT_SECRET_FILE = client_secrect_file
    SCOPES = scopes
    creds = None

    # if token file exist, create creditials from it
    if os.path.exists('api/token.json'):
        creds = Credentials.from_authorized_user_file('api/token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('api/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        print('An error occurred: %s' % error)

    print('service created successfully')
    return service


SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = 'api/credentials.json'

def create_calendar():
  service = create_service(CLIENT_SECRET_FILE, SCOPES)

  event_body = {
    "summary": "My 4th Event hahaha",
    "location": "313 G2",
    "description": "3 tín \n Th.S. Nguyễn Anh Thư",
    "end": {
      "dateTime": "2022-05-06T22:00:00",
      "timeZone": "Asia/Ho_Chi_Minh"
    },
    "start": {
      "dateTime": "2022-05-06T21:00:00",
      "timeZone": "Asia/Ho_Chi_Minh"
    },
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }

  event = service.events().insert(calendarId='primary', body=event_body).execute()
  print('Event created: %s' % (event.get('htmlLink')))