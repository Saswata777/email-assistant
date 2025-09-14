# app.py

import os
import urllib.parse
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

# --- New Imports for Auth ---
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google.auth.exceptions

# --- Your existing backend imports ---
from backend.db import (
    init_db, create_or_update_user, get_user_by_google_id,
    get_emails, get_email_by_id, mark_as_sent, save_email
)
from backend.gmail_client import fetch_latest_emails, send_email_reply
# (Assuming these are your AI/processing modules)
from backend.processing import categorize_email
from backend.rag import query_docs
from backend.llm import generate_response

# --- Auth Configuration ---
CLIENT_SECRETS_FILE = "backend/credentials.json" # Assumes client_secret.json is in the backend folder
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]
REDIRECT_URI = "http://localhost:8000/auth/callback" # Must match Google Cloud Console
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # For local dev ONLY

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # DELETED: The old scheduler thread is gone
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# --- Helper to get user credentials ---
def get_user_credentials(user_google_id: str) -> Credentials:
    user = get_user_by_google_id(user_google_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    client_config = flow.client_config

    return Credentials.from_authorized_user_info(
        info={
            "refresh_token": user.refresh_token,
            "client_id": client_config["client_id"],
            "client_secret": client_config["client_secret"],
            "token_uri": client_config["token_uri"],
        },
        scopes=SCOPES
    )

# --- NEW: Authentication Endpoints ---
@app.get("/login")
async def login():
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    if 'error' in request.query_params:
        error_details = request.query_params.get('error')
        return JSONResponse(
            status_code=400,
            content={"message": "Authentication failed or was cancelled by the user.", "error": error_details}
        )
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    flow.fetch_token(code=request.query_params.get("code"))
    creds = flow.credentials
    
    service = build('oauth2', 'v2', credentials=creds)
    user_info = service.userinfo().get().execute()
    google_id = user_info['id']
    email = user_info['email']
    
    # user = create_or_update_user(google_id, email, creds.refresh_token)
    
    user = create_or_update_user(google_id, email, creds.refresh_token)
    
    # NEW: Instead of returning JSON, we redirect back to the frontend
    # We will send the user's ID as a URL parameter
    frontend_url = "http://localhost:3000/auth/callback"
    params = urllib.parse.urlencode({"user_google_id": user.google_id})
    
    return RedirectResponse(url=f"{frontend_url}?{params}")
    
    # In a real app, you would set a session cookie and redirect to your frontend dashboard
    # For now, we return the user's Google ID so the frontend knows who they are
    # return JSONResponse({"message": "Authentication successful", "user_google_id": user.google_id})

# --- NEW: Endpoint to replace the scheduler ---
@app.post("/sync-emails/{user_google_id}")
async def sync_emails(user_google_id: str):
    user = get_user_by_google_id(user_google_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    creds = get_user_credentials(user_google_id)
    try:
        # This is the logic from your old scheduler.py
        emails_from_gmail = fetch_latest_emails(creds, max_results=5)
        saved_count = 0
        for mail in emails_from_gmail:
            # Add deduplication logic here if needed
            priority, sentiment = categorize_email(mail["subject"], mail["body"])
            context_docs = query_docs(mail["body"], top_k=3) if mail["body"] else []
            ai_reply = generate_response(mail["body"], context_docs)
            
            save_email(
                user_id=user.id, # Pass the user's DB id
                sender=mail["sender"],
                subject=mail["subject"],
                body=mail["body"],
                priority=str(priority),
                sentiment=str(sentiment),
                ai_reply=ai_reply
            )
            saved_count += 1
        return {"status": "success", "message": f"{saved_count} emails synced and processed."}
    except google.auth.exceptions.RefreshError:
        raise HTTPException(status_code=401, detail="Token expired or revoked. Please re-login.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# --- MODIFIED: Your existing endpoints now need the user's ID ---

@app.get("/emails/{user_google_id}")
async def list_emails(user_google_id: str):
    user = get_user_by_google_id(user_google_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_emails(user.id) # Pass the user's DB id

@app.get("/emails/{user_google_id}/{email_id}")
async def email_detail(user_google_id: str, email_id: int):
    user = get_user_by_google_id(user_google_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    email = get_email_by_id(email_id, user.id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

# Stats endpoint also needs to be user-specific
@app.get("/stats/{user_google_id}")
async def stats(user_google_id: str):
    user = get_user_by_google_id(user_google_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    emails = get_emails(user.id)
    # ... your existing stats logic ...
    total = len(emails)
    urgent = sum(1 for e in emails if e.priority == "high")
    normal = sum(1 for e in emails if e.priority == "normal")
    resolved = sum(1 for e in emails if e.status == "sent")
    pending = sum(1 for e in emails if e.status == "pending")

    return { "total": total, "urgent": urgent, "resolved": resolved, "pending": pending, "normal": normal }

class ReplyRequest(BaseModel):
    user_google_id: str
    email_id: int
    reply: str

@app.post("/send-reply")
async def send_reply(data: ReplyRequest):
    user = get_user_by_google_id(data.user_google_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    email = get_email_by_id(data.email_id, user.id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found or does not belong to user")

    try:
        creds = get_user_credentials(data.user_google_id)
        send_email_reply(creds, email.sender, email.subject, data.reply)
        mark_as_sent(data.email_id, user.id, data.reply)
        return {"status": "success", "message": "Reply sent successfully"}
    except google.auth.exceptions.RefreshError:
        raise HTTPException(status_code=401, detail="Token expired or revoked. Please re-login.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
