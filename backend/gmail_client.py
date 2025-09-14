# backend/gmail_client.py

import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials # Important import

# DELETED: SCOPES, BASE_DIR, CREDENTIALS_PATH, TOKEN_PATH - These are now managed in app.py
# DELETED: authenticate_gmail() function - This is replaced by the web flow in app.py

def extract_body(payload):
    """(Your existing function - no changes needed)"""
    # ... (same code as you had)
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and "data" in part["body"]:
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
            elif "parts" in part:
                text = extract_body(part)
                if text:
                    return text
    elif "data" in payload.get("body", {}):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
    return ""

# MODIFIED: Now requires a credentials object
def fetch_latest_emails(credentials: Credentials, max_results=5):
    """Fetch latest emails using the provided user credentials."""
    service = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        full_msg = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = full_msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")
        body = extract_body(full_msg["payload"])
        emails.append({"sender": sender, "subject": subject, "body": body})

    return emails

# MODIFIED: Now requires a credentials object
def send_email_reply(credentials: Credentials, to, subject, body):
    """Send a reply email using the provided user credentials."""
    service = build("gmail", "v1", credentials=credentials)
    msg = MIMEText(body)
    msg["to"] = to
    msg["subject"] = f"Re: {subject}"
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    message = {"raw": raw_message}
    sent_msg = service.users().messages().send(userId="me", body=message).execute()
    return sent_msg