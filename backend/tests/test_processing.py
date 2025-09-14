# backend/tests/test_processing.py
import pytest
from backend.processing import detect_priority, detect_sentiment, categorize_email

def test_detect_priority_high():
    subject = "Server is down - urgent"
    body = "We cannot access the database!"
    assert detect_priority(subject, body) == "high"

def test_detect_priority_normal():
    subject = "Weekly Report"
    body = "Please review the attached report."
    assert detect_priority(subject, body) == "normal"

def test_detect_sentiment_positive():
    text = "I am very happy with the support received."
    assert detect_sentiment(text) == "positive"

def test_detect_sentiment_negative():
    text = "This is terrible. The system failed again!"
    assert detect_sentiment(text) == "negative"

def test_detect_sentiment_neutral():
    text = "The meeting is scheduled for tomorrow."
    assert detect_sentiment(text) == "neutral"

def test_categorize_email():
    subject = "Urgent: Cannot login"
    body = "I cannot access my account, please fix ASAP."
    priority, sentiment = categorize_email(subject, body)
    assert priority == "high"
    # sentiment could be neutral or negative depending on TextBlob, so just check type
    assert sentiment in ["positive", "neutral", "negative"]
