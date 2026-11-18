#!/usr/bin/env python3
"""
YouTube Data API v3 Helper with robust retry logic
"""

import os
import sys
import time
import argparse
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.join(SCRIPT_DIR, "client_secrets.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")


def get_authenticated_service():
    creds = None
    if os.environ.get("YOUTUBE_TOKEN_JSON") and not os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "w") as f:
            f.write(os.environ["YOUTUBE_TOKEN_JSON"])

    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"Error loading existing token: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            for attempt in range(4):
                try:
                    print(f"Refreshing expired credentials (attempt {attempt + 1})...")
                    creds.refresh(Request())
                    with open(TOKEN_FILE, "w") as token:
                        token.write(creds.to_json())
                    break
                except Exception as e:
                    print(f"Refresh failed: {e}. Retrying in 2 seconds...")
                    time.sleep(2)
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"Error: {CLIENT_SECRETS_FILE} not found.")
                sys.exit(1)

            print("Initiating OAuth login flow...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=False, prompt="consent")
            
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
            print(f"Authentication successful! Token saved to {TOKEN_FILE}")

    return build("youtube", "v3", credentials=creds)


def upload_short(file_path, title, description="", tags=None, privacy="public"):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    if tags is None:
        tags = ["Shorts", "GTA6", "Gaming"]

    if "#Shorts" not in title and "#shorts" not in title:
        title = f"{title} #Shorts"

    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "20"
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print(f"Uploading '{title}'...")
    response = None
    for attempt in range(4):
        try:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")
            if response:
                break
        except Exception as e:
            print(f"Upload chunk error: {e}. Retrying in 2 seconds...")
            time.sleep(2)

    if response:
        print(f"Upload complete! Video ID: {response.get('id')}")
        print(f"Link: https://youtube.com/shorts/{response.get('id')}")
    return response


def main():
    parser = argparse.ArgumentParser(description="YouTube Automation CLI")
    parser.add_argument("--upload", type=str, help="Upload a video/short file")
    parser.add_argument("--title", type=str, default="GTA 6 Epic Moment #Shorts", help="Title")
    parser.add_argument("--description", type=str, default="", help="Description")
    parser.add_argument("--tags", type=str, default="GTA6,Shorts,Gaming,Hindi", help="Comma-separated tags")
    parser.add_argument("--privacy", type=str, default="private", choices=["public", "unlisted", "private"])

    args = parser.parse_args()

    if args.upload:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        upload_short(args.upload, args.title, args.description, tags, args.privacy)


if __name__ == "__main__":
    main()
