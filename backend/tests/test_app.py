# backend/tests/test_app.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Import your app and database objects
from backend.app import app
from backend.db import Base, engine, SessionLocal, User, Email

# Create a test client
client = TestClient(app)

# --- Test Data ---
# We'll use this fake user ID for all our tests
FAKE_USER_GOOGLE_ID = "123456789-fake-user"
FAKE_USER_EMAIL = "testuser@example.com"


# --- Fixtures ---

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """
    This fixture runs before each test. It drops and recreates the database
    so that each test starts with a clean slate.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Yields a database session for direct manipulation in tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_user(db_session):
    """Creates a fake user in the database for tests to use."""
    user = User(
        google_id=FAKE_USER_GOOGLE_ID,
        email=FAKE_USER_EMAIL,
        refresh_token="fake-refresh-token"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# --- Tests ---

def test_get_emails_for_new_user(test_user):
    """
    Tests that a newly created user has no emails initially.
    """
    response = client.get(f"/emails/{FAKE_USER_GOOGLE_ID}")
    assert response.status_code == 200
    assert response.json() == []


def test_get_emails_for_nonexistent_user():
    """
    Tests that requesting emails for a user who doesn't exist returns a 404 error.
    """
    response = client.get("/emails/nonexistent-user-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_add_emails_and_get_stats(db_session, test_user):
    """
    Tests adding emails for a user and then fetching them and their stats.
    """
    # We add emails directly to the DB for this test to isolate the API logic
    email1 = Email(user_id=test_user.id, sender="sender1@test.com", subject="Urgent Email", body="...", priority="high", status="pending", sentiment="negative")
    email2 = Email(user_id=test_user.id, sender="sender2@test.com", subject="Normal Email", body="...", priority="normal", status="pending", sentiment="neutral")
    email3 = Email(user_id=test_user.id, sender="sender3@test.com", subject="Resolved Email", body="...", priority="normal", status="sent", sentiment="positive")
    
    db_session.add_all([email1, email2, email3])
    db_session.commit()

    # 1. Test the /emails/{user_id} endpoint
    response_emails = client.get(f"/emails/{FAKE_USER_GOOGLE_ID}")
    assert response_emails.status_code == 200
    emails_data = response_emails.json()
    assert len(emails_data) == 3
    assert emails_data[0]["subject"] == "Urgent Email"

    # 2. Test the /stats/{user_id} endpoint
    response_stats = client.get(f"/stats/{FAKE_USER_GOOGLE_ID}")
    assert response_stats.status_code == 200
    stats_data = response_stats.json()
    assert stats_data["total"] == 3
    assert stats_data["urgent"] == 1
    assert stats_data["resolved"] == 1
    assert stats_data["pending"] == 2
    assert stats_data["normal"] == 2

    # 3. Test the /emails/{user_id}/{email_id} detail endpoint
    response_detail = client.get(f"/emails/{FAKE_USER_GOOGLE_ID}/{email1.id}")
    assert response_detail.status_code == 200
    assert response_detail.json()["priority"] == "high"


# Using @patch to "mock" the external gmail sending function
@patch("backend.app.send_email_reply")
def test_send_reply(mock_send_email, db_session, test_user):
    """
    Tests the send-reply endpoint by mocking the actual email sending function.
    """
    # Setup: Create an email to reply to
    email = Email(user_id=test_user.id, sender="sender@test.com", subject="Test Subject", body="Test body", status="pending")
    db_session.add(email)
    db_session.commit()

    reply_data = {
        "user_google_id": FAKE_USER_GOOGLE_ID,
        "email_id": email.id,
        "reply": "This is my test reply."
    }

    # Make the API call
    response = client.post("/send-reply", json=reply_data)

    # Assertions
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify that our mocked email sending function was called correctly
    mock_send_email.assert_called_once()

    # Verify that the email status was updated in the database
    db_session.refresh(email)
    assert email.status == "sent"
    assert email.ai_reply == "This is my test reply."