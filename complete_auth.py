#!/usr/bin/env python3
"""
Complete OAuth flow via code or redirect URL
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


def exchange_code(code_or_url, redirect_uri="http://localhost:8080/"):
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    code = code_or_url.strip()
    if "code=" in code:
        parsed = urlparse(code)
        params = parse_qs(parsed.query)
        if "code" in params:
            code = params["code"][0]

    flow.fetch_token(code=code)
    creds = flow.credentials

    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

    print("SUCCESS: Token saved successfully to token.json!")
    return creds


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 complete_auth.py '<redirect_url_or_code>'")
        sys.exit(1)
    exchange_code(sys.argv[1])
