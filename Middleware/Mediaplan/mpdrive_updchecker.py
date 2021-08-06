from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import fnmatch
import io
import json
from googleapiclient.http import MediaIoBaseDownload


# this is the scope permission you can review more about this on: https://developers.google.com/drive/api/v3/about-auth?hl=en
SCOPES = ['https://www.googleapis.com/auth/drive']
#you need to have the token.json files created by the quickstart: https://developers.google.com/drive/api/v3/quickstart/python
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('drive', 'v3', credentials=creds)
mediacomFolder_id = '1FXHM94WqnMa18pnz-ysuXhVMbJyzaPsR'

query = f"mimeType = 'application/vnd.google-apps.folder' and \'{mediacomFolder_id}\' in parents"
results = service.files().list(q=query,
                                fields="nextPageToken, files(id, name)").execute()

def fileinFolder(folder_id, folder_name):
    month_list =[]
    monthid_list = []
    query = f" \'{folder_id}\' in parents"
    results = service.files().list(q=query,
                                    fields='nextPageToken, files(id, name)').execute()

    subitems = results.get('files', [])
    for subitem in subitems:
        print(subitem['name'])
        query = f" \'{subitem['id']}\' in parents"
        results = service.files().list(q=query,
                                        fields='nextPageToken, files(id, name)').execute()
        files = results.get('files', [])
        for file in files:
            month_list.append(file['name'])
            monthid_list.append(file['id'])
            print(u'{0} ({1})'.format(file['name'], file['id']))
    month_dict = {monthid_list[i]: month_list[i] for i in range(len(month_list))}
    return month_dict

def file_down(file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))

    fh.seek(0)

    with open (os.path.join('drive_downloads/', file_name), 'wb') as f:
        f.write(fh.read())
        f.close()

n = 1
ff_list =[]
months = results.get('files', [])
for month in months:
    print('Folders:')
    print(month.get('name'))
    print(n)
    n = n+1
    print("files in ", month['name'], ":")
    ff_list.append(fileinFolder(month['id'], month['name']))

mco_json = {'folders': months, 'subitems':ff_list}
#crea el archivo json de respaldo diario
with open ("mco_mpdrive.json", 'w') as json_file:
    json.dump(mco_json, json_file)

down = int(input())-1
for i in ff_list[down]:
    print(i)

print('¿Cuáles quieres descargar?: 1. Cierres 2. Planes')
select = input()
if select == '1':
    for i in ff_list[down]:
        if "Mediaplan" in ff_list[down][i]:
            if "Cierre" in ff_list[down][i]:
                print(ff_list[down][i])
                file_down(i, ff_list[down][i])
elif select == '2':
    print('Planes')
    for i in ff_list[down]:
        if "Cierre" not in ff_list[down][i]:
            if "Mediaplan" in ff_list[down][i]:
                print(ff_list[down][i])
                file_down(i, ff_list[down][i])
else:
    print('quepedo')
