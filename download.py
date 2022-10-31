# https://developers.google.com/drive/api/guides/api-specific-auth
# https://developers.google.com/drive/api/quickstart/python
# https://developers.google.com/drive/api/guides/manage-downloads
import hashlib
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, DEFAULT_CHUNK_SIZE

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


OUT_PATH = "/data/reason/vist"
if not os.path.exists(OUT_PATH):
    os.makedirs(OUT_PATH)


def get_sha1_file_buffer(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


class MediaIoDownload(MediaIoBaseDownload):
    def __init__(self, file_path, request, chunksize=DEFAULT_CHUNK_SIZE):
        progress = 0
        if os.path.exists(file_path):
            self._file_path = file_path
            fd = open(file_path, "ab")
            progress = os.path.getsize(file_path)
            print(f"Resuming download at {progress / 1024 / 1024:.2f} MB")
        else:
            self._file_path = file_path
            fd = open(file_path, "wb")
        super().__init__(fd, request, chunksize)
        self._progress = progress

    def close(self):
        self._fd.close()


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    with open("file_list.txt") as f:
        lines = f.readlines()
    items = [line.strip().split() for line in lines if line.strip()]
    print("Files:")
    for item in items:
        print(item[0], item[1])

    print("\n-------\nstart to download\n-------")
    for item in items:
        name, file_id, sha1sum = item
        save_path = os.path.join(OUT_PATH, name)
        print(f"\nDownloading {name} to {save_path}")
        max_resume_try = 3
        n_resume_try = 0
        while True:
            n_resume_try += 1
            if n_resume_try > max_resume_try:
                print(f"Failed to download {name}")
                break
            if os.path.exists(save_path):
                print("File already exists, checking sha1sum...")
                file_hash = get_sha1_file_buffer(save_path)
                if file_hash == sha1sum:
                    print(f"File {name} already exists and is correct.")
                    break
                else:
                    print(f"The hash is not correct. Resume download {name}.")
            try:
                service_files = service.files()
                request = service_files.get_media(fileId=file_id)
                max_try = 10
                downloader = MediaIoDownload(save_path, request)
                done = False
                retry = 0
                while done is False:
                    try:
                        status, done = downloader.next_chunk()
                        print(
                            f"Download {name}: {status.progress() * 100 : .2f}%.",
                            end="\r",
                        )
                    except Exception as e:
                        if retry < max_try:
                            print(f"Retry {retry} times.", end="\r")
                            retry += 1
                            continue
                        else:
                            raise e
                    retry = 0
            except Exception as e:
                print(e)
            finally:
                downloader.close()


if __name__ == "__main__":
    main()
