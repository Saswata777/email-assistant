# db.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

DB_PATH = os.getenv("DATABASE_PATH", "./inbox.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# 1. NEW: User table to store each user's credentials
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    refresh_token = Column(String, nullable=False)
    emails = relationship("Email", back_populates="owner")



class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    
    # 2. ADDED: Link to the User table
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="emails")
    
    
    sender = Column(String, index=True)
    subject = Column(String, index=True)
    body = Column(Text)
    priority = Column(String, default="normal")  # low, normal, high
    sentiment = Column(String, default="neutral")  # positive, neutral, negative
    ai_reply = Column(Text, default="")  # AI-generated reply
    received_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, approved, sent

def init_db():
    """Create tables in the database"""
    # Base.metadata.create_all(bind=engine)
    Base.metadata.create_all(bind=engine, checkfirst=True)
    

# 3. NEW: Functions to manage users
def create_or_update_user(google_id: str, email: str, refresh_token: str):
    db = SessionLocal()
    user = db.query(User).filter(User.google_id == google_id).first()
    if user:
        user.refresh_token = refresh_token
    else:
        user = User(google_id=google_id, email=email, refresh_token=refresh_token)
        db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user    

def get_user_by_google_id(google_id: str):
    db = SessionLocal()
    user = db.query(User).filter(User.google_id == google_id).first()
    db.close()
    return user
    
    
    

def get_emails(user_id: int):
    """Fetch all emails"""
    db = SessionLocal()
    emails = db.query(Email).filter(Email.user_id == user_id).all()
    db.close()
    return emails

def get_email_by_id(email_id: int, user_id: int):
    """Fetch a single email by ID"""
    db = SessionLocal()
    email = db.query(Email).filter(Email.id == email_id, Email.user_id == user_id).first()
    db.close()
    return email

def save_email(user_id: int, sender, subject, body, priority="normal", sentiment="neutral", ai_reply=""):
    db = SessionLocal()
    email = Email(
        user_id=user_id, # Link the email to the user
        sender=sender,
        subject=subject,
        body=body,
        priority=priority,
        sentiment=sentiment,
        ai_reply=ai_reply
    )
    db.add(email)
    db.commit()
    db.refresh(email)
    db.close()
    return email

def mark_as_sent(email_id: int, user_id: int, final_reply: str):
    db = SessionLocal()
    email = db.query(Email).filter(Email.id == email_id, Email.user_id == user_id).first()
    if email:
        email.ai_reply = final_reply
        email.status = "sent"
        db.commit()
        db.refresh(email)
    db.close()
    return email

