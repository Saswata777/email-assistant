AI-Powered Email Assistant (Inbox-IQ)An AI-powered solution to automate and streamline support email management. It uses NLP to categorize, prioritize, and generate intelligent responses, all displayed on a clean, intuitive dashboard.Key FeaturesAutomated Email Filtering: Fetches and filters support emails via the Gmail API.AI-Powered Triage: Uses an LLM for sentiment analysis and urgency detection.Intelligent Auto-Responses: Generates context-aware replies using a RAG pipeline and a knowledge base.Centralized Dashboard: A Next.js frontend displays emails, analytics, and drafted responses for review.Scheduled Fetching: Periodically checks for new emails via a background scheduler.Project StructureThe project is organized into a Python backend for core logic and a Next.js frontend for the user interface.Email-Assistant/
│
├── .gitignore
├── backend/
│   ├── app.py
│   ├── gmail_client.py     # Handles Gmail API communication
│   ├── processing.py
│   ├── rag.py              # Retrieval-Augmented Generation pipeline
│   ├── llm.py              # Interface with the Gemini LLM
│   ├── db.py
│   ├── scheduler.py        # Background task scheduler
│   ├── requirements.txt
│   ├── tests/
│   ├── credentials.json    # Google API credentials (DO NOT COMMIT)
│   ├── token.pkl           # Google API token (DO NOT COMMIT)
│   └── .env                # Environment variables (DO NOT COMMIT)
│
├── kb/
│   └── (Contains Markdown/PDF documents for the knowledge base)
│
├── inbox-iq/               # Next.js frontend application
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
├── inbox.db
│
└── README.md
Technologies UsedBackend: Python, Flask, Gemini API, Google Gmail API, SQLite, APSchedulerFrontend: Next.js, React, Tailwind CSSCore Concepts: NLP, RAG, REST APIsGetting StartedPrerequisitesPython 3.9+Node.js and npm/yarnGoogle Cloud Platform project with Gmail API enabledAccess to the Gemini APIInstallation & SetupClone the repositorygit clone [https://github.com/your-username/Email-Assistant.git](https://github.com/your-username/Email-Assistant.git)
cd Email-Assistant
Backend Setupcd backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Set up your .env file and credentials.json
Frontend Setupcd ../inbox-iq
npm install
# Set up your frontend environment variables if any
Run the applicationStart the backend Flask server.Start the frontend Next.js development server.
