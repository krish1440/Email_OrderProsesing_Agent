import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class OrderExtractor:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment!")
        
        genai.configure(api_key=api_key)
        # Using the latest stable Flash model
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def extract_order_details(self, email_body):
        """
        Uses Gemini to extract structured data from unstructured email text.
        """
        prompt = f"""
        You are an expert order processing assistant. 
        Read the following email and extract the order details.
        The email might be messy, contain HTML tags, or be a long conversation. 
        Focus ONLY on the actual purchase details.
        
        Return the data strictly in JSON format with these exact keys:
        - order_id: (Look for numbers like #1234 or "Order 1234". Use "N/A" if missing)
        - customer_name: (Full name of the person buying)
        - customer_email: (Their contact email)
        - product_name: (The main product purchased, e.g., "iPhone")
        - quantity: (The number of items purchased)
        - items: (A summary string of all items)
        - total_amount: (The final price paid)
        - date: (The date of the order)

        Email Content:
        ---
        {email_body}
        ---
        
        Return ONLY the JSON. No conversational text.
        """

        try:
            response = self.model.generate_content(prompt)
            # Clean the response text (remove ```json and ```)
            text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return {
                "order_id": "Error",
                "customer_name": "Error",
                "customer_email": "Error",
                "items": "Error during extraction",
                "total_amount": "N/A",
                "date": "N/A"
            }
