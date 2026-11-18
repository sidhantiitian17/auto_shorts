#!/usr/bin/env python3
"""
Runs a local server to automatically capture OAuth authorization
"""

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.join(SCRIPT_DIR, "client_secrets.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")

def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )
    print("STARTING_SERVER", flush=True)
    # run_local_server starts listening immediately and prints the URL
    creds = flow.run_local_server(
        port=8080,
        prompt="consent",
        access_type="offline",
        authorization_prompt_message="Open this URL in your browser to sign in:\n{url}\n"
    )

    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())
    print("\nSUCCESS: Authorization complete! Token saved.", flush=True)

if __name__ == "__main__":
    main()
