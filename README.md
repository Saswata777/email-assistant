# 📧 Inbox-IQ: AI-Powered Email Assistant

**Inbox-IQ** is an AI-powered solution to automate and streamline support email management.  
It leverages **Natural Language Processing (NLP)** and **Retrieval-Augmented Generation (RAG)** to categorize, prioritize, and generate intelligent responses — all accessible through a clean, intuitive dashboard.

---

## 🚀 Key Features

- **Automated Email Filtering**  
  Fetches and filters support emails via the **Gmail API**.

- **AI-Powered Triage**  
  Uses an **LLM** for sentiment analysis and urgency detection.

- **Intelligent Auto-Responses**  
  Generates **context-aware replies** using a **RAG pipeline** and a **knowledge base**.

- **Centralized Dashboard**  
  A **Next.js frontend** displays emails, analytics, and drafted responses for review.

- **Scheduled Fetching**  
  Periodically checks for new emails via a background scheduler.

---
Video Representation:

[![Watch the video](link-to-your-preview-image.png)](https://drive.google.com/file/d/15wdpquJZ-BPKimzi3yWKIdABFHEPj9Mk/view?usp=sharing)
---

## 📂 Project Structure

```plaintext
Email-Assistant/
│
├── .gitignore
├── backend/
│   ├── app.py               # Flask app entrypoint
│   ├── gmail_client.py      # Handles Gmail API communication
│   ├── processing.py        # Email preprocessing & categorization
│   ├── rag.py               # Retrieval-Augmented Generation pipeline
│   ├── llm.py               # Interface with Gemini LLM
│   ├── db.py                # SQLite database integration
│   ├── scheduler.py         # Background task scheduler
│   ├── requirements.txt     # Python dependencies
│   ├── tests/               # Unit & integration tests
│   ├── credentials.json     # Google API credentials (DO NOT COMMIT)
│   ├── token.pkl            # Gmail API token (DO NOT COMMIT)
│   └── .env                 # Environment variables (DO NOT COMMIT)
│
├── kb/                      # Knowledge base (Markdown/PDF docs)
│
├── inbox-iq/                # Next.js frontend application
│   └── src/
│       └── app/
│           ├── api.js
│           ├── auth/
│           ├── components/
│           ├── favicon.ico
│           ├── globals.css
│           ├── layout.js
│           └── page.js
│
├── inbox.db                 # SQLite database file
│
└── README.md
```

---


## 🛠️ Technologies Used

- **Backend**: Python, Flask, Gemini API, Google Gmail API, SQLite, APScheduler  
- **Frontend**: Next.js, React, Tailwind CSS  
- **Core Concepts**: NLP, RAG, REST APIs  

---

## ⚙️ Getting Started

### ✅ Prerequisites
- Python **3.9+**
- Node.js and npm/yarn
- Google Cloud Platform project with **Gmail API enabled**
- Access to the **Gemini API**

---

### 🔧 Installation & Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Email-Assistant.git
cd Email-Assistant
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Activate the virtual environment
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

 Configure frontend environment variables if required.

 #### ▶️ Running the Application
 #### Start the Backend (Flask)
```bash
cd backend
python -m uvicorn backend.app:app --reload -- 8000
```

#### Start the Frontend (Next.js)

```bash
cd inbox-iq
npm run dev
```



