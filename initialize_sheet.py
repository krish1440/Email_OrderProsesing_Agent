import os
from services.google_auth import GoogleService
from services.sheets_handler import SheetsHandler
from dotenv import load_dotenv

load_dotenv()

def initialize_sheet():
    print("--- Initializing Google Sheet Headers ---")
    try:
        google_service = GoogleService()
        sheets = SheetsHandler(google_service.get_sheets_service())
        
        # Order: Date, Order ID, Name, Email, Product Name, Quantity, Total, Status, Link
        headers = [
            "Date", 
            "Order ID", 
            "Customer Name", 
            "Customer Email", 
            "Product Name", 
            "Quantity", 
            "Total Price", 
            "Status", 
            "Email Link"
        ]
        
        sheets.initialize_headers(headers)
        print("SUCCESS: Headers created in Google Sheet.")
        
    except Exception as e:
        print(f"FAILED: {str(e)}")

if __name__ == "__main__":
    initialize_sheet()
