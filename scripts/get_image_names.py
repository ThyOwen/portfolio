import os, argparse
from PIL import Image

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

parser = argparse.ArgumentParser()

parser.add_argument("-g", "--google_drive_folder_id", help = "the code in the google drive url that identifies the drive", required=True, type=str)
parser.add_argument("-v", "--verification_path", help = "path to token.json and credentials.json", required=True, type=str)
parser.add_argument("-p", "--output_path_str", help = "the reletive path containing the thumbnail images. ex: ./assets/my/Filmz/Swideo2024", required=True, type=str)

args = parser.parse_args()

token_path = os.path.join(args.verification_path, 'token.json')
credentials_path = os.path.join(args.verification_path, 'credentials.json')

folder_id = args.google_drive_folder_id
output_path = args.output_path_str

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


creds = None

if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

try:
    service = build('drive', 'v3', credentials=creds)
except HttpError as error:
    print(f'An error occurred: {error}')

# %%
import pandas as pd

print("starting")

query = f"parents = '{folder_id}'"

response = service.files().list(pageSize=1000, q = query).execute()
files = response.get('files')

df = pd.DataFrame(files)#.sort_values("name", ignore_index=True)

print(df)

# %%

with open('files.txt', 'w') as f:
    for idx in range(len(df)):
        link = df['id'][idx]
        file = df['name'][idx]
        f.write('<a href = "https://drive.google.com/file/d/' + link + '/view"> <img class="img-responsive" src= "' + output_path + '/_' + file + '" alt="Image ' + str(idx) + '"></a>\n')
