from __future__ import print_function
import email
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from datetime import datetime
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    'GET https://gmail.googleapis.com/gmail/v1/users/{userId}/messages'

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label)

    print("-----------------------------------------------")
    print("-----------------------------------------------")

    # print("time before 1: ", datetime.now().time())
    # show_chatty_threads(service, 'me')
    # print("time after 1: ", datetime.now().time())
    print("time before 2: ", datetime.now().time())
    get_messages(service, 'me')
    print("time after 2: ", datetime.now().time())

# Get messages


def get_messages(service, user_id='me'):
    try:
        messages = service.users().messages().list(
            userId=user_id, q='in:sent after:2018/01/01 before:2021/05/01').execute()

        print("Email: ", messages)

    except Exception as error:
        print('An error occurred: %s' % error)

    return messages


def show_chatty_threads(service, user_id='me'):
    threads = service.users().threads().list(
        userId=user_id).execute().get('threads', [])
    for thread in threads:
        tdata = service.users().threads().get(
            userId=user_id, id=thread['id']).execute()
        nmsgs = len(tdata['messages'])
        print("message count:", nmsgs)

    print("thread len: ", len(threads))

    # if nmsgs >= 1:    # skip if <3 msgs in thread
    #     msg = tdata['messages'][0]['payload']
    #     subject = ''
    #     for header in msg['headers']:
    #         if header['name'] == 'Subject':
    #             subject = header['value']
    #             break
    #     if subject:  # skip if no Subject line
    #         print('- %s (%d msgs)' % (subject, nmsgs))


if __name__ == '__main__':
    main()
