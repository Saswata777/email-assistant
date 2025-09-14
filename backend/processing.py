# processing.py
from textblob import TextBlob

# 🔹 Priority keywords
URGENT_KEYWORDS = ["urgent", "immediately", "asap", "cannot access", "critical", "failed"]

def detect_priority(subject: str, body: str) -> str:
    """Detects priority from subject/body based on keywords."""
    text = f"{subject.lower()} {body.lower()}"
    for keyword in URGENT_KEYWORDS:
        if keyword in text:
            return "high"
    return "normal"

def detect_sentiment(text: str) -> str:
    """Basic sentiment analysis using TextBlob."""
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.2:
        return "positive"
    elif analysis.sentiment.polarity < -0.2:
        return "negative"
    else:
        return "neutral"

def categorize_email(subject: str, body: str):
    """Returns (priority, sentiment) tuple for an email."""
    priority = detect_priority(subject, body)
    sentiment = detect_sentiment(f"{subject} {body}")
    return priority, sentiment
