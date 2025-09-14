import pytest
from backend.db import (
    Base, 
    engine, 
    SessionLocal,
    User, # Import User model
    create_or_update_user,
    get_user_by_google_id,
    save_email,
    get_emails,
    get_email_by_id,
    mark_as_sent
)

# --- Fixtures ---

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """
    This fixture runs before each test. It ensures that every test
    starts with a fresh, empty database.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provides a database session to the tests."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Tests for User Functions ---

def test_create_and_get_user(db_session):
    """Tests creating a new user and retrieving them."""
    # 1. Create a user
    user = create_or_update_user("google_id_123", "test@example.com", "token_abc")
    assert user.google_id == "google_id_123"
    assert user.email == "test@example.com"
    
    # 2. Retrieve the user and verify
    fetched_user = get_user_by_google_id("google_id_123")
    assert fetched_user is not None
    assert fetched_user.id == user.id
    assert fetched_user.refresh_token == "token_abc"

def test_update_user_token():
    """Tests that calling create_or_update_user again updates the token."""
    # 1. Create the initial user
    create_or_update_user("google_id_123", "test@example.com", "token_abc")
    
    # 2. Call the function again with the same ID but a new token
    updated_user = create_or_update_user("google_id_123", "test@example.com", "token_xyz_new")
    
    # 3. Verify the token was updated
    fetched_user = get_user_by_google_id("google_id_123")
    assert fetched_user.refresh_token == "token_xyz_new"

def test_get_nonexistent_user():
    """Tests that getting a non-existent user returns None."""
    fetched_user = get_user_by_google_id("non_existent_id")
    assert fetched_user is None

# --- Tests for Email Functions (Multi-User Context) ---

def test_save_and_get_emails_for_specific_user():
    """
    Tests that emails are correctly saved and retrieved for the correct user,
    and not for other users.
    """
    # 1. Create two different users
    user1 = create_or_update_user("user1_google", "user1@test.com", "token1")
    user2 = create_or_update_user("user2_google", "user2@test.com", "token2")

    # 2. Save an email specifically for user1
    save_email(
        user_id=user1.id,
        sender="sender@example.com",
        subject="User1 Email",
        body="This is a test for user1."
    )

    # 3. Get emails for user1 and verify
    user1_emails = get_emails(user_id=user1.id)
    assert len(user1_emails) == 1
    assert user1_emails[0].subject == "User1 Email"

    # 4. Get emails for user2 and verify they have no emails
    user2_emails = get_emails(user_id=user2.id)
    assert len(user2_emails) == 0

def test_get_email_by_id_security():
    """
    Tests that a user can only retrieve an email by ID if they are the owner.
    """
    # 1. Create two users
    user1 = create_or_update_user("user1_google", "user1@test.com", "token1")
    user2 = create_or_update_user("user2_google", "user2@test.com", "token2")

    # 2. Save an email for user1
    email = save_email(user_id=user1.id, sender="a@a.com", subject="Private Email", body="...")

    # 3. Verify user1 can fetch their own email
    fetched_by_owner = get_email_by_id(email_id=email.id, user_id=user1.id)
    assert fetched_by_owner is not None
    assert fetched_by_owner.subject == "Private Email"

    # 4. Verify user2 CANNOT fetch user1's email
    fetched_by_other = get_email_by_id(email_id=email.id, user_id=user2.id)
    assert fetched_by_other is None

def test_mark_as_sent_for_specific_user():
    """Tests that an email is correctly marked as sent for the owner."""
    # 1. Create a user and an email
    user = create_or_update_user("user1_google", "user1@test.com", "token1")
    email = save_email(user_id=user.id, sender="a@a.com", subject="Test", body="...")
    assert email.status == "pending" # Check initial state

    # 2. Mark the email as sent
    final_reply = "This issue is now resolved."
    mark_as_sent(email_id=email.id, user_id=user.id, final_reply=final_reply)

    # 3. Fetch the email again and verify its status and reply
    updated_email = get_email_by_id(email_id=email.id, user_id=user.id)
    assert updated_email.status == "sent"
    assert updated_email.ai_reply == final_reply