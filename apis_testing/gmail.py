from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

import os

from . import utils

# If modifying these scopes, delete the file token.pickle.

"""Send an email message from the user's account.
"""

import base64
import email
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

# extracts message from gmail message Object
def extract_message(message):
  msg = {
    'id': message['id'],
    'date': message['internalDate'],
  }
  # print('working')
  for header in message['payload']['headers']:
    if header['name'] == 'to' or header['name'] == 'To':
      msg['to'] = header['value']
    elif header['name'] == 'from' or header['name'] == 'From':
      msg['from'] = header['value']
    elif header['name'] == 'subject' or header['name'] == 'Subject':
      msg['subject'] = header['value']
    elif header['name'] == 'Message-Id':
      msg['msg_id'] = header['value']
  # print('working')
  if (message['payload']['mimeType'] == 'text/plain' or message['payload']['mimeType'] == 'text/html') and message['payload']['filename'] == '':
    msg['body'] = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
  elif message['payload']['mimeType'] == "multipart/alternative" and message['payload']['filename'] == '':
    msg['body'] = base64.urlsafe_b64decode(message['payload']['parts'][1]['body']['data']).decode('utf-8')
  elif message['payload']['mimeType'] == 'multipart/mixed' and message['payload']['filename'] == '':
    msg['body'] = base64.urlsafe_b64decode(message['payload']['parts'][0]['parts'][1]['body']['data']).decode('utf-8')
  
  return msg

def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    message = service.users().messages().get(userId=user_id, id=message['id']).execute()
    return extract_message(message)
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def CreateMessage(sender, to, subject, message_text, threadId=None, in_reply_to=None, references=None):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  message['In-Reply-To'] = in_reply_to
  message['References'] = references
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode(), 'threadId': threadId}


def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
  filename, threadId=None, in_reply_to=None, references=None):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  message['In-Reply-To'] = in_reply_to
  message['References'] = references

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string()), 'threadId': threadId}

"""Get a list of Messages from the user's mailbox.
"""

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print('Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetShortMessage(service, user_id, msg_id):
    message = None
    try:
        message = GetMessage(service, user_id, msg_id)
    except:
        print('No such message')
    if message is not None:
        return {
            'id': message['id'],
            'snippet': message['snippet'],
            'date': message['internalDate'],
            'threadId': message['threadId'],
            'headers': message['payload']['headers']
        }
    return {
        'id': '',
        'snippet': '',
        'date': '',
        'threadId': '',
        'headers': []
    }

def ListMessagesMatchingQuery(service, user_id, query='from:domailhannah@gmail.com'):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(
        userId=user_id,
        q=query
    ).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    # return messages
    snip_msgs = []
    for msg in messages:
        snip_msgs.append(GetShortMessage(service, user_id, msg['id']))
    return snip_msgs
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def ListMessagesWithLabels(service, user_id, label_ids=[]):
  """List all Messages of the user's mailbox with label_ids applied.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.

  Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
  try:
    response = service.users().messages().list(
      userId=user_id,
      labelIds=label_ids
    ).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(
        userId=user_id,
        labelIds=label_ids,
        pageToken=page_token
      ).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    print('Message snippet: %s' % message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetThreadDetails(service, user_id, thread_id):
  """Get a Thread.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    thread_id: The ID of the Thread required.

  Returns:
    Thread with matching ID.
  """
  try:
    thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
    print(thread)
    final_thread = {
      'id': thread['id'],
      'messages': []
    }
    # print(final_thread)
    for message in thread['messages']:
      msg = extract_message(message)
      final_thread['messages'].append(msg)
    return final_thread
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetThread(service, user_id, thread_id):
  """Get a Thread.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    thread_id: The ID of the Thread required.

  Returns:
    Thread with matching ID.
  """
  try:
    thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
    # final_thread = {
    #   'id': thread['id'],
    #   'internalDate': thread['internalDate'],
    #   'messages': []
    # }
    # for message in thread['messages']:
    #   msg = {}
    #   if 'to' or 'To' in message['headers']:
    #     msg['to'] = message['headers']['to'] or message['headers']['To']
    #   if 'from' or 'From' in message['headers']:
    #     msg['from'] = message['headers']['from'] or message['headers']['From']
    #   if 'subject' or 'Subject' in message['headers']:
    #     msg['subject'] = message['headers']['subject'] or message['headers']['Subject']
    #   msg['msg_id'] = message['headers']['Message-Id']

    #   # fetch and decode the body
    #   if message['payload']['mimeType'] == 'text/plain' and message['payload']['body'] and message['payload']:
    #     msg['body'] = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
    #   elif message


    #   final_thread['messages'].append(msg)
    # return final_thread
    return thread
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetThreadHeaders(service, user_id, thread_id):
  """Get a Thread.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    thread_id: The ID of the Thread required.

  Returns:
    Thread with matching ID.
  """
  try:
    thread = service.users().threads().get(userId=user_id, id=thread_id, format='metadata', metadataHeaders=['from', 'to', 'subject', 'date']).execute()
    # messages = thread['messages']
    # print ('thread id: %s - number of messages '
    #        'in this thread: %d') % (thread['id'], len(messages))
    return {
      'id': thread['id'],
      'snippet': thread['messages'][0]['snippet'],
      'date': thread['messages'][0]['internalDate'],
      'headers': thread['messages'][0]['payload']['headers'],
      'message_count': len(thread['messages'])
    }
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


"""Get a list of Threads from the user's mailbox.
"""
def ListThreadsMatchingQuery(service, user_id, query=''):
  """List all Threads of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
           Eg.- 'label:UNREAD' for unread messages only.

  Returns:
    List of threads that match the criteria of the query. Note that the returned
    list contains Thread IDs, you must use get with the appropriate
    ID to get the details for a Thread.
  """
  try:
    response = service.users().threads().list(userId=user_id, q=query).execute()
    threads = []
    # print(len(response['threads']))
    if 'threads' in response:
      threads.extend(response['threads'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().threads().list(userId=user_id, q=query,
                                        pageToken=page_token).execute()
      threads.extend(response['threads'])
      # print(len(response['threads']))
    threads_with_headers = []
    for thread in threads:
      # print(thread['id'])
      threads_with_headers.append(GetThreadHeaders(service, user_id, thread['id']))
    return threads_with_headers
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def GetAttachments(service, user_id, msg_id, store_dir):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    for part in message['payload']['parts']:
      if part['filename']:

        file_data = base64.urlsafe_b64decode(part['body']['data']
                                             .encode('UTF-8'))

        path = ''.join([store_dir, part['filename']])

        f = open(path, 'w')
        f.write(file_data)
        f.close()

  except errors.HttpError as error:
    print('An error occurred: %s' % error)

def run_api(user):
    creds = None

    try:
        creds = utils.load_credentials(user)
        print(creds)
    except ObjectDoesNotExist:
        print('No matching query')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(settings.BASE_DIR, 'credentials.json'),
                settings.GMAIL_SCOPES,
                redirect_uri=settings.REDIRECT_URI
            )
            creds = flow.run_local_server(port=8001)
    
    utils.save_credentials(user, creds)

    service = build('gmail', 'v1', credentials=creds)

    return service