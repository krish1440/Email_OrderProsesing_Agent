import time
import sys
import os
from services.google_auth import GoogleService
from services.gmail_handler import GmailHandler
from services.sheets_handler import SheetsHandler
from services.extractor import OrderExtractor

# Force UTF-8 for Windows Terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def run_agent():
    print("--- Email Order Agent Starting ---")
    
    try:
        # 1. Initialize Services
        google_service = GoogleService()
        gmail = GmailHandler(google_service.get_gmail_service())
        sheets = SheetsHandler(google_service.get_sheets_service())
        ai = OrderExtractor()
        
        # 2. Fetch Unread Emails with "New Order" in subject
        print("Checking for new orders (Subject: 'New Order')...")
        query = 'is:unread subject:"New Order"'
        messages = gmail.get_unread_emails(query=query)
        
        if not messages:
            print("No new orders found.")
            return

        print(f"Found {len(messages)} unread 'New Order' emails. Filtering for ID pattern...")
        
        processed_count = 0
        for msg_info in messages:
            msg_id = msg_info['id']
            
            # 3. Get Content and Check for #ID
            email_data = gmail.get_email_content(msg_id)
            if "#" not in email_data['subject']:
                print(f"  > Skipping: {email_data['subject']} (No #ID found)")
                continue
                
            print(f"  > Processing: {email_data['subject']}")
            
            # 4. AI Extraction
            order = ai.extract_order_details(email_data['body'])
            
            # --- Fallbacks ---
            # Fallback for Order ID from Subject (look for # followed by numbers)
            order_id = order.get('order_id')
            if not order_id or order_id == "N/A":
                import re
                id_match = re.search(r'#(\d+)', email_data['subject'])
                order_id = id_match.group(1) if id_match else "N/A"

            # Fallback for Date from Gmail Timestamp
            order_date = order.get('date')
            if not order_date or order_date == "N/A":
                order_date = email_data['date']

            # Fallback for Email
            customer_email = order.get('customer_email')
            if not customer_email or customer_email == "N/A":
                customer_email = email_data['sender_email']

            # 5. Prepare Sheet Data
            # Ensure items and other fields are strings (prevents Sheets API 400 errors)
            items_str = str(order.get('items', 'N/A'))
            
            sheet_row = [
                str(order_date),
                str(order_id),
                str(order.get('customer_name', 'N/A')),
                str(customer_email),
                items_str,
                str(order.get('total_amount', 'N/A')),
                "New",
                f"https://mail.google.com/mail/u/0/#inbox/{msg_id}"
            ]
            
            # 6. Append to Sheet
            sheets.append_row(sheet_row)
            print(f"    Added to Sheet: {order.get('customer_name')}")
            
            # 7. Mark as Read
            gmail.mark_as_read(msg_id)
            print(f"    Email processed.")
            
        print("\n--- All Orders Processed ---")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    run_agent()
