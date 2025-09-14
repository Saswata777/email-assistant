# # scheduler.py
# import time
# from backend.gmail_client import fetch_latest_emails
# from backend.db import save_email, init_db
# from backend.processing import categorize_email
# from backend.rag import query_docs
# from backend.llm import generate_response

# POLL_INTERVAL = 60  # seconds

# def run_scheduler():
#     print("📩 Inbox scheduler started...")
#     init_db()

#     seen_subjects = set()  # simple deduplication (can use message_id later)

#     while True:
#         try:
#             emails = fetch_latest_emails(max_results=5)
#             for mail in emails:
#                 if mail["subject"] not in seen_subjects:
                    
#                     subject = (mail.get("subject") or "").strip()
#                     body = (mail.get("body") or "").strip()

#                     # 🚨 Skip if no real content
#                     if not subject and not body:
#                         print("⚠️ Skipping empty email")
#                         continue
                    
                    
#                     # 1️⃣ Analyze + categorize
#                     priority, sentiment = categorize_email(subject, body)

#                     # 2️⃣ Retrieve relevant KB docs
#                     context_docs = query_docs(body, top_k=3) if body else []

#                     # 3️⃣ Generate AI reply using Google Generative AI
#                     try:
#                         ai_reply = generate_response(body, context_docs)
#                     except Exception as e:
#                         print(f"⚠️ Failed to generate AI reply: {e}")
#                         ai_reply = ""

#                     # 4️⃣ Save to DB
#                     save_email(
#                         sender=mail["sender"],
#                         subject=subject,
#                         body=body,
#                         priority=priority,
#                         sentiment=sentiment,
#                         ai_reply=ai_reply
#                     )

#                     seen_subjects.add(subject)
#                     print(f"✅ Saved: {subject} [{priority}, {sentiment}]")
#                     if ai_reply:
#                         print(f"🤖 AI Reply generated:\n{ai_reply}\n")

#         except Exception as e:
#             print("⚠️ Error in scheduler:", e)

#         time.sleep(POLL_INTERVAL)


# if __name__ == "__main__":
#     run_scheduler()
