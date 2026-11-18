#!/usr/bin/env python3
"""
OAuth Authorization Generator and Token Handler
"""

import os
import sys
import json
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.join(SCRIPT_DIR, "client_secrets.json")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "token.json")


def generate_auth_url():
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"Error: {CLIENT_SECRETS_FILE} missing.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8080/"
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    print("=" * 60)
    print("PLEASE OPEN THIS URL IN YOUR BROWSER TO AUTHORIZE:")
    print("=" * 60)
    print(auth_url)
    print("=" * 60)
    return flow, auth_url


if __name__ == "__main__":
    generate_auth_url()
