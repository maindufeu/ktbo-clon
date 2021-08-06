from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import fnmatch
import io
from googleapiclient.http import MediaIoBaseDownload


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
#flow = InstalledAppFlow.from_client_secrets_file(
#    'credentials.json', SCOPES)
#creds = flow.run_local_server(port=0)
# Save the credentials for the next run
#with open('token.json', 'w') as token:
#    token.write(creds.to_json())
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('drive', 'v3', credentials=creds)
mediacomFolder_id = '1FXHM94WqnMa18pnz-ysuXhVMbJyzaPsR'


query = "mimeType = 'application/vnd.google-apps.folder' and '1SUmf4QGyeuRmtgmo5NmXNHuirL48nHqn' in parents"

results = service.files().list(q=query,
                                fields="nextPageToken, files(id, name)").execute()

mco_files  ={'':''}
pattern = '2021'
for file in results.get('files', []):
    #print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    if fnmatch.fnmatch(file.get('name'), pattern):
        print(file.get('id'))

folder = results.get('files', [])
print('Folders:')
for item in folder:
    print(u'{0} ({1})'.format(item['name'], item['id']))

results = service.files().list(q="'1DM7xldNc54XAIFfb_abV3r1IboN9rFmD' in parents",
                                          fields='nextPageToken, files(id, name)').execute()

items = results.get('files', [])
print('Files:')
for item in items:
    print(u'{0} ({1})'.format(item['name'], item['id']))


#creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#service = build('drive', 'v3', credentials=creds)

file_id = '1squEh1oMnRPtwVZVU1C7ubUzCArIoeg1'
request = service.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print ("Download %d%%." % int(status.progress() * 100))

fh.seek(0)

with open (os.path.join('./Middleware/Mediaplan/drive_downloads', "2020_ktbo_kube_Adverity_Mediaplan_Octubre-Caricam.xlsx"), 'wb') as f:
    f.write(fh.read())
    f.close()
