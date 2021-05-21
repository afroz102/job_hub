
from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os.path
import datetime
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle


SERVICE_ACCOUNT_FILE = 'credentials.json'


CALENDER_SCOPES = ['https://www.googleapis.com/auth/calendar']


# For Help visit:
# https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322
def getCalender():
    flow = InstalledAppFlow.from_client_secrets_file(
        SERVICE_ACCOUNT_FILE, scopes=CALENDER_SCOPES)

    credentials = flow.run_console()

    pickle.dump(credentials, open("token.pkl", "wb"))
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)

    result = service.calendarList().list().execute()
    print("Calender Api: ", result)

    return result


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def getCalenderData():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(
            'token.json', CALENDER_SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SERVICE_ACCOUNT_FILE, CALENDER_SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    return events
