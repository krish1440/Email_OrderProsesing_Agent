# Technical Setup & Client Transfer Guide

This document tracks every detail needed to set up and transfer this project to a client.

## 1. Google Cloud Console (The Client's Identity)
The client must eventually own this project to avoid using your API quotas.

### Steps for Client:
1.  **Create Project:** Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  **Enable APIs:**
    *   `Gmail API`
    *   `Google Sheets API`
3.  **Create Credentials:**
    *   Create a **Service Account** (Recommended for automation).
    *   Download the `credentials.json` file.
    *   **Grant Access:** The client must share their target Google Sheet with the Service Account email (found inside `credentials.json`).

## 2. GitHub Secrets (Secure Configuration)
Since we are using GitHub Actions, we NEVER put passwords or API keys in the code. We put them in **Settings > Secrets and variables > Actions**.

### Required Secrets:
| Secret Name | Description |
|-------------|-------------|
| `GEMINI_API_KEY` | The API key for extraction brain. |
| `GOOGLE_CREDENTIALS_BASE64` | The contents of `credentials.json` (encoded in Base64). |
| `SPREADSHEET_ID` | The ID of the target Google Sheet. |

## 3. Local Development Setup
To run this script on your machine during development:

1.  **Python Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  **Environment Variables (`.env`):**
    Create a `.env` file (this is git-ignored):
    ```env
    GEMINI_API_KEY=your_key
    SPREADSHEET_ID=your_sheet_id
    ```

## 4. Troubleshooting & Small Details
- **Email Processing:** The agent only looks for `is:unread` emails. If you want to re-process an email, mark it as unread in Gmail.
- **Quota Limits:** Gmail API has a rate limit; daily runs are well within the free tier.
- **Scopes:** Ensure the Google App is set to "Internal" or "Testing" to avoid full verification processes.

---
*This guide will be updated as we build the project.*
