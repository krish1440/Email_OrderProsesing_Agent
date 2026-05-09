# Project: Email Reading Agent (Order Automator)

## What This Is
An automated agent designed to read Gmail messages, extract order details (even from unstructured text) using AI, and append them to a Google Sheet. It runs daily via GitHub Actions.

## Core Value
Eliminate manual data entry of orders. The agent is built to be "Client-Transferable," meaning it can be easily handed over to the client by simply swapping API credentials.

## Tech Stack
- **Language:** Python 3.10+
- **Email Access:** Gmail API (OAuth2 / Service Account)
- **Extraction Brain:** Gemini Pro API (for template-agnostic extraction)
- **Database:** Google Sheets API (Primary) / Excel (Fallback)
- **Scheduler:** GitHub Actions (Daily Cron)

## Requirements

### Active
- [ ] Connect to Gmail API and fetch unread emails.
- [ ] Use Gemini AI to extract structured JSON (Name, Date, Items, Price) from raw email text.
- [ ] Append extracted data to a Google Sheet.
- [ ] Mark email as "Processed" (Read) to prevent duplicate entries.
- [ ] Daily automation setup using GitHub Actions Secrets.
- [ ] Robust error handling and logging.

### Out of Scope
- Real-time processing (switched to daily for simplicity and cost).
- Complex CRM integrations (keeping it simple: Sheet-based).

## Key Decisions
| Decision | Rationale | Outcome |
|----------|-----------|---------|
| **Gemini AI** | Handles emails without templates; more robust than regex. | Pending |
| **Google Sheets** | Easier for clients to access and multi-user friendly. | Pending |
| **GitHub Actions** | Zero cost for small volumes; built-in scheduler. | Pending |

---
*Last updated: 2026-05-09*
