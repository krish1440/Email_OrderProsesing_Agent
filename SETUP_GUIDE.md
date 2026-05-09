# 🚀 Client Setup Guide: Email Order Automator

This guide will help you set up the automation from scratch. No coding knowledge is required—just follow the steps.

---

## Phase 1: Google Cloud Setup (The "Brain")
1.  **Open the Console:** Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  **Create Project:** Click "Select a project" at the top -> **New Project**. Name it "Order Automator".
3.  **Enable APIs:** Search for these two in the top bar and click **Enable** for both:
    *   `Gmail API`
    *   `Google Sheets API`
4.  **OAuth Consent Screen:**
    *   Search for "OAuth consent screen". Select **External** -> **Create**.
    *   Fill in "App name" (Order Bot) and your email. Click Save.
    *   **IMPORTANT:** Go to the "Test users" section, click **Add Users**, and type in your own email address.
5.  **Download Keys:**
    *   Go to **Credentials** -> **Create Credentials** -> **OAuth client ID** -> **Desktop app**.
    *   Download the JSON file, rename it to `client_secret.json`, and put it in the project folder.

---

## Phase 2: Google Sheets Setup (The "Database")
1.  **Create a Service Account:**
    *   Go to **Credentials** -> **Create Credentials** -> **Service Account**.
    *   Name it "Sheet Bot" and click **Done**.
    *   Click on the email address of the new Service Account -> **Keys** tab -> **Add Key** -> **Create new key (JSON)**.
    *   Download this file, rename it to `credentials.json`, and put it in the project folder.
2.  **Share your Sheet:**
    *   Open your Google Sheet.
    *   Click **Share** (top right).
    *   Paste the email address of your Service Account (found in Phase 2, Step 1) and give it **Editor** permissions.

---

## Phase 3: Authorization (One-Time Step)
1.  **Generate Token:** Open your terminal in the project folder and run:
    `python get_gmail_token.py`
2.  **Login:** A browser window will open. Log in with your Gmail account and click **Allow**. 
3.  You will now see a file called `token.json` in your folder. **Do not delete it!**

---

## Phase 4: Going Live (GitHub Automation)
If you want this to run every day automatically:
1.  **Get a Gemini Key:** Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and click **Create API Key**.
2.  **GitHub Secrets:** In your GitHub Repository, go to **Settings > Secrets and variables > Actions**.
3.  Add these 4 "New repository secrets":
    *   `SPREADSHEET_ID`: (The long ID in your Google Sheet URL)
    *   `GEMINI_API_KEY`: (Your Gemini Key from Step 1)
    *   `GOOGLE_CREDENTIALS_BASE64`: (Content of `credentials.json` turned into Base64)
    *   `GMAIL_TOKEN_BASE64`: (Content of `token.json` turned into Base64)

---

## 🛠️ Troubleshooting
*   **"Order ID is N/A":** Ensure the email subject contains a `#` followed by numbers (e.g., #5544).
*   **"Permission Denied":** Double-check that you shared the Google Sheet with the Service Account email.
*   **"Token Expired":** If it stops working after 7 days, make sure you clicked **"Publish App"** in the OAuth Consent Screen in Google Console.

---
*Last updated: May 2026*
