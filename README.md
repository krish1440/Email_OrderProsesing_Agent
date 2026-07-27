# Email Order Processing Agent

An intelligent Python-based automation agent that processes incoming order emails, extracts order details using AI, and automatically logs them into a Google Sheet for streamlined order management.

## 📋 Overview

The **Email Order Processing Agent** is designed to:
- Monitor your Gmail inbox for new order emails (with "New Order" subject line)
- Extract structured order information from unstructured email content using Google Gemini AI
- Automatically append order details to a Google Sheet for centralized tracking
- Handle fallback mechanisms for missing data (e.g., extracting Order ID from email subject)
- Mark processed emails as read to avoid duplicates

## ✨ Key Features

### 1. **Email Monitoring**
- Fetches unread emails with "New Order" subject line from Gmail
- Filters emails that contain order ID pattern (#ID)
- Supports OAuth 2.0 authentication for secure Gmail access

### 2. **AI-Powered Data Extraction**
- Uses Google Gemini AI (gemini-2.5-flash) to intelligently parse email content
- Extracts structured order data from messy, unformatted email text
- Handles complex scenarios like HTML-formatted emails and multi-part messages

### 3. **Google Sheets Integration**
- Automatically appends extracted order data to a designated Google Sheet
- Uses Google Service Account credentials for reliable authentication
- Supports batch appending with proper formatting

### 4. **Smart Fallback Logic**
- **Order ID**: Falls back to pattern matching (#number) in email subject if AI extraction fails
- **Order Date**: Uses Gmail timestamp if not found in email content
- **Customer Email**: Uses sender's email address if not extracted from body

### 5. **Data Fields Captured**
Each order record includes:
- **Date**: Order date (from email timestamp)
- **Order ID**: Order identifier (from subject or email body)
- **Customer Name**: Full name of the customer
- **Customer Email**: Contact email address
- **Product Name**: Primary product ordered
- **Quantity**: Number of items
- **Total Amount**: Final price/total cost
- **Status**: Order status (default: "New")
- **Email Link**: Direct link back to the original Gmail message

## 🏗️ Architecture

### Project Structure
```
Email_OrderProsesing_Agent/
├── main.py                      # Main entry point for the agent
├── services/
│   ├── google_auth.py          # OAuth & Service Account authentication
│   ├── gmail_handler.py        # Gmail API operations
│   ├── sheets_handler.py       # Google Sheets API operations
│   └── extractor.py            # Gemini AI-based order extraction
├── get_gmail_token.py          # Gmail OAuth token generation script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Module Descriptions

#### `main.py`
The core orchestrator that:
- Initializes all services (Gmail, Sheets, Gemini)
- Fetches unread "New Order" emails
- Processes each email through the AI extraction pipeline
- Handles fallback mechanisms for incomplete data
- Appends results to Google Sheet and marks emails as read

#### `services/google_auth.py`
Handles authentication for both Gmail and Sheets:
- **Gmail Authentication**: Uses OAuth 2.0 token (token.json)
- **Sheets Authentication**: Uses Service Account credentials
- Supports Base64-encoded credentials for GitHub Actions
- Manages token refresh and expiration

#### `services/gmail_handler.py`
Gmail API wrapper providing:
- `get_unread_emails()`: Fetch unread messages by query
- `get_email_content()`: Extract subject, body, sender, and timestamp
- `mark_as_read()`: Mark emails as read after processing

#### `services/sheets_handler.py`
Google Sheets API wrapper providing:
- `append_row()`: Add new row to sheet with order data
- `initialize_headers()`: Set up column headers for the sheet

#### `services/extractor.py`
AI-powered order extraction using Gemini:
- Uses `gemini-2.5-flash` model for fast, accurate extraction
- Parses unstructured email content into JSON format
- Returns standardized order object with 7 key fields
- Includes error handling with fallback responses

#### `get_gmail_token.py`
Utility script for setting up Gmail OAuth:
- Generates initial `token.json` file
- Requires `client_secret.json` from Google Console
- Run once before first use: `python get_gmail_token.py`

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- Google Account with Gmail and Google Sheets access
- Google Cloud Project with Gmail and Sheets APIs enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/krish1440/Email_OrderProsesing_Agent.git
   cd Email_OrderProsesing_Agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials**
   
   a. Create a Google Cloud Project and enable:
   - Gmail API
   - Google Sheets API
   - Google Generative AI API

   b. Download credentials:
   - **Gmail OAuth**: Download `client_secret.json` (Desktop app credentials)
   - **Sheets Service Account**: Download `credentials.json`
   - **Gemini API Key**: Generate from Google AI Studio

4. **Generate Gmail token**
   ```bash
   python get_gmail_token.py
   ```
   - Opens browser for OAuth authentication
   - Creates `token.json` file

5. **Create environment file (.env)**
   ```env
   GEMINI_API_KEY=your-gemini-api-key-here
   SPREADSHEET_ID=your-google-sheet-id-here
   ```

### Configuration

#### Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | API key for Google Gemini | `AIzaSyD...` |
| `SPREADSHEET_ID` | Google Sheet ID to append orders | `1a2B3c4D5e...` |
| `GMAIL_TOKEN_BASE64` | (Optional) Base64-encoded token.json for CI/CD | |
| `GOOGLE_CREDENTIALS_BASE64` | (Optional) Base64-encoded credentials.json for CI/CD | |

#### Google Sheet Setup
1. Create a new Google Sheet
2. Share it with your Service Account email
3. Add headers to the first row (optional - agent can work without them):
   ```
   Date | Order ID | Customer Name | Email | Product Name | Quantity | Total Amount | Status | Email Link
   ```

### Running the Agent

```bash
python main.py
```

Expected output:
```
--- Email Order Agent Starting ---
Checking for new orders (Subject: 'New Order')...
Found 2 unread 'New Order' emails. Filtering for ID pattern...
  > Processing: New Order #1001
    Added to Sheet: John Doe
    Email processed.
  > Processing: New Order #1002
    Added to Sheet: Jane Smith
    Email processed.

--- All Orders Processed ---
```

## 🔄 Email Format Requirements

For optimal processing, emails should:

1. **Have "New Order" in subject line**
   ```
   Subject: New Order #1001
   ```

2. **Include an Order ID** (one of these formats)
   - `#1234` (most common)
   - `Order 1234`
   - `ID: 1234`

3. **Contain order details** (AI will find these)
   - Customer name
   - Product information
   - Quantity
   - Price/Total amount
   - Email address

### Example Email Format
```
From: customer@example.com
Subject: New Order #1001

Hi,

I would like to place an order for:

Product: iPhone 15 Pro
Quantity: 2
Total: $2,399.98

Customer Name: John Doe
Email: john@example.com

Thanks!
```

## 🐛 Error Handling

The agent implements robust error handling:

1. **Missing Fields**: Falls back to alternative extraction methods
2. **Parsing Errors**: Returns "N/A" for fields that couldn't be extracted
3. **Network Issues**: Graceful exception handling with informative error messages
4. **Invalid Credentials**: Clear error messages directing user to setup

## 🔐 Security

- **OAuth 2.0**: Gmail uses secure OAuth for access without storing passwords
- **Service Account**: Sheets uses Service Account (keyfile-based) authentication
- **Base64 Encoding**: Credentials can be Base64-encoded for secure CI/CD environments
- **No Password Storage**: No hardcoded credentials in code
- **.env Support**: Sensitive data stored in environment variables

## 🛠️ Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| google-api-python-client | 2.126.0 | Gmail & Sheets API client |
| google-auth | 2.29.0 | OAuth 2.0 authentication |
| google-auth-oauthlib | 1.2.0 | OAuth flow management |
| google-generativeai | 0.5.2 | Gemini AI API |
| python-dotenv | 1.0.1 | Environment variable management |
| openpyxl | 3.1.2 | Excel/spreadsheet support (optional) |

## 📝 Troubleshooting

### Issue: `token.json not found! Run 'python get_gmail_token.py' first.`
**Solution**: Execute the token generation script and complete OAuth authentication.

### Issue: `SPREADSHEET_ID not set in environment!`
**Solution**: Create `.env` file with `SPREADSHEET_ID=your-sheet-id`

### Issue: `GEMINI_API_KEY not found in environment!`
**Solution**: Add `GEMINI_API_KEY=your-key` to `.env` file

### Issue: No emails are processed
**Possible Causes**:
- No unread emails with "New Order" subject
- Emails don't contain #ID pattern
- Incorrect Gmail query
**Solution**: Check email subject line and content match requirements

### Issue: Empty or incorrect data in Sheet
**Cause**: Email format doesn't contain expected data
**Solution**: Refer to "Email Format Requirements" section above

## 🔮 Future Enhancements

- [ ] Support for multiple email providers (Outlook, Yahoo Mail)
- [ ] Advanced scheduling (cron jobs, webhooks)
- [ ] Email attachment handling (invoices, attachments)
- [ ] Multi-language support for email parsing
- [ ] Advanced error recovery and retry mechanisms
- [ ] Slack/Discord notifications for new orders
- [ ] Custom field mapping for Google Sheets
- [ ] Order status update workflows
- [ ] Database integration (PostgreSQL, MongoDB)
- [ ] REST API for external integrations

## 📊 Workflow Diagram

```
Unread Gmail → Filter by → Extract Order → Append to → Mark as
   Inbox      "New Order"   Details (AI)   Google Sheets   Read
```

## 📄 License

This project is private and owned by krish1440.

## 👤 Author

**Krishna** - [GitHub Profile](https://github.com/krish1440)

## 🤝 Contributing

For bug reports, feature requests, or contributions, please contact the repository owner.

## 📞 Support

For issues or questions:
1. Check the "Troubleshooting" section above
2. Review the code comments in each service module
3. Check environment variable configuration
4. Verify Google Cloud project setup

---

**Last Updated**: May 2026  
**Repository**: [Email_OrderProsesing_Agent](https://github.com/krish1440/Email_OrderProsesing_Agent)
