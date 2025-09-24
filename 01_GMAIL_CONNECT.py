import os
import datetime
import email
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] # Define required scopes
ATTACHMENTS = '/Users/dustincremascoli/Automation/Raise/FILES_RAISE/'
creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
messages = results.get('messages', [])

msg_id_dataset = []

if not messages:
    print('No messages found.')
else:
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload_headers = msg['payload']['headers']
        for item in payload_headers:
            if item['name'] == 'From':
                from_clean = item['value'].split(' ')[-1].lstrip('<').rstrip('>')
                if from_clean == 'syw-transformco-external-reports@raise.com':
                    msg_id_dataset.append(message['id'])

for msg_id in msg_id_dataset:
    msg = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
    msg_raw = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    mail = email.message_from_bytes(msg_raw)

    for part in mail.walk():
        if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if not filename:
            filename = f'part-{counter:03d}.bin'

        if filename.split('.')[-1] == 'pdf':
            att_path = os.path.join(ATTACHMENTS , filename[:31] + '.pdf')
            if not os.path.isfile(att_path):
                with open(att_path, 'wb') as fp:
                    fp.write(part.get_payload(decode=True))
        else:
            continue
