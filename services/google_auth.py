import os
import json
import base64
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class GoogleService:
    def __init__(self):
        # Scopes for Gmail (OAuth) and Sheets (Service Account)
        self.gmail_scopes = ['https://www.googleapis.com/auth/gmail.modify']
        self.sheet_scopes = ['https://www.googleapis.com/auth/spreadsheets']

    def get_gmail_service(self):
        """
        Uses token.json (OAuth 2.0) for Gmail.
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.gmail_scopes)
        else:
            # Fallback to Base64 for GitHub Actions
            token_base64 = os.getenv('GMAIL_TOKEN_BASE64')
            if token_base64:
                token_info = json.loads(base64.b64decode(token_base64))
                creds = Credentials.from_authorized_user_info(token_info, self.gmail_scopes)
        
        # Refresh if expired (only if we have creds and they are valid for refresh)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        if not creds:
            raise Exception("token.json not found! Run 'python get_gmail_token.py' first.")
            
        return build('gmail', 'v1', credentials=creds)

    def get_sheets_service(self):
        """
        Uses credentials.json (Service Account) for Sheets.
        """
        if os.path.exists('credentials.json'):
            creds = service_account.Credentials.from_service_account_file(
                'credentials.json', scopes=self.sheet_scopes
            )
        else:
            creds_base64 = os.getenv('GOOGLE_CREDENTIALS_BASE64')
            if not creds_base64:
                raise Exception("credentials.json or GOOGLE_CREDENTIALS_BASE64 not found!")
            creds_info = json.loads(base64.b64decode(creds_base64))
            creds = service_account.Credentials.from_service_account_info(
                creds_info, scopes=self.sheet_scopes
            )
            
        return build('sheets', 'v4', credentials=creds)
