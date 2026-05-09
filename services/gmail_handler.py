class GmailHandler:
    def __init__(self, service):
        self.service = service

    def get_unread_emails(self, query="is:unread"):
        """
        Fetches list of unread emails based on query.
        """
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        return messages

    def get_email_content(self, msg_id):
        """
        Retrieves the body text of a specific email.
        """
        message = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender_raw = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")
        
        # Extract clean email from "Name <email@example.com>"
        import re
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', sender_raw)
        sender_email = email_match.group(0) if email_match else sender_raw

        # Extract body
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    import base64
                    data = part['body'].get('data', '')
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        else:
            import base64
            data = payload['body'].get('data', '')
            body = base64.urlsafe_b64decode(data).decode('utf-8')

        # Get Internal Date
        import datetime
        timestamp = int(message.get('internalDate', 0)) / 1000
        email_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        return {
            'id': msg_id,
            'subject': subject,
            'sender_email': sender_email,
            'body': body,
            'date': email_date
        }

    def mark_as_read(self, msg_id):
        """
        Removes the 'UNREAD' label from the email.
        """
        self.service.users().messages().modify(
            userId='me', 
            id=msg_id, 
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
