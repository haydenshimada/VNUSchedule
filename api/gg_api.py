from calendar import calendar
import datetime
from math import remainder
import os.path
import flask

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_service(client_secrect_file, scopes):
	# Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
	# flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
	# 	client_secrect_file, scopes=scopes)
	flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=client_secrect_file, scopes=scopes)
	flow.redirect_uri = 'http://localhost:8080'
	creds = flow.run_console()

	print('success')
	# The URI created here must exactly match one of the authorized redirect URIs
	# for the OAuth 2.0 client, which you configured in the API Console. If this
	# value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
	# error.
	# flow.redirect_uri = 'http://localhost:8080'

	# # Use the authorization server's response to fetch the OAuth 2.0 tokens.
	# authorization_response = flask.request.url
	# flow.fetch_token(authorization_response=authorization_response)

	# creds = flow.credentials

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

  event = service.events().insert(calendarId='primary', body=event_body).execute()
  print('Event created: %s' % (event.get('htmlLink')))



event_body = {
    "summary": "My 4th Event hahaha",
    "location": "313 G2",
    "description": "3 tín \n Th.S. Nguyễn Anh Thư",
    "end": {
      "dateTime": "2022-05-04T22:00:00",
      "timeZone": "Asia/Ho_Chi_Minh"
    },
    "start": {
      "dateTime": "2022-05-04T21:00:00",
      "timeZone": "Asia/Ho_Chi_Minh"
    },
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }