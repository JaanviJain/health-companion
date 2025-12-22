import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailHealthIntegration:
    def __init__(self, credentials_path: str):
        self.creds = None
        self.credentials_path = credentials_path
        self.service = None

    def authenticate(self):
        """Authenticate with Gmail API"""
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(f"Could not find {self.credentials_path}. Did you download it from Google Cloud?")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('gmail', 'v1', credentials=self.creds)

    def get_health_emails(self, max_results=10):
        """Fetch health-related emails"""
        # Search queries for common health providers or keywords
        queries = [
            'subject:(lab results) has:attachment',
            'subject:(medical report) has:attachment',
            'subject:(test results) has:attachment'
        ]
        
        all_messages = []
        try:
            for query in queries:
                print(f"🔍 Searching Gmail for: {query}")
                results = self.service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=max_results
                ).execute()
                
                messages = results.get('messages', [])
                all_messages.extend(messages)
                
            print(f"✅ Found {len(all_messages)} potential health emails.")
            return all_messages
        except Exception as e:
            print(f"❌ Gmail Search Error: {e}")
            return []

    def extract_email_content(self, message_id: str):
        """Get full email content and extract attachments"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            payload = message.get('payload', {})
            headers = payload.get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
            
            attachments = self._get_attachments(message)
            
            return {
                'id': message_id,
                'subject': subject,
                'date': date,
                'attachments': attachments
            }
        except Exception as e:
            print(f"❌ Error extracting email {message_id}: {e}")
            return None

    def _get_attachments(self, message):
        """Extract and download attachments"""
        attachments = []
        parts = message.get('payload', {}).get('parts', [])
        
        # Iterate through email parts to find files
        # Note: Emails can be nested, but we'll stick to top-level for simplicity
        for part in parts:
            if part.get('filename') and part.get('body') and part['body'].get('attachmentId'):
                att_id = part['body']['attachmentId']
                filename = part['filename']
                
                # Filter for useful files only
                if filename.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                    print(f"   📎 Found attachment: {filename}")
                    attachment = self.service.users().messages().attachments().get(
                        userId='me',
                        messageId=message['id'],
                        id=att_id
                    ).execute()
                    
                    file_data = base64.urlsafe_b64decode(attachment['data'])
                    attachments.append({
                        'filename': filename,
                        'data': file_data
                    })
                    
        return attachments