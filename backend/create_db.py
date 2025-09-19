# create_db.py

from backend.db import engine, Base
import os

# This is a safety check. It's often better to handle DB creation/migration
# outside of a simple script like this in production (e.g., with Alembic),
# but for this project, this script is a clear and simple solution.
print("--- Database Initializer ---")

# Check if the database file already exists.
db_path = os.getenv("DATABASE_PATH", "./inbox.db")
if os.path.exists(db_path):
    print(f"Database file found at '{db_path}'.")
    print("Skipping table creation as it might already be set up.")
    print("If you need to recreate tables, delete the .db file and run this script again.")
else:
    print(f"No database file found. Creating tables in '{db_path}'...")
    # This command connects to the database and creates all tables
    # defined in your models that inherit from Base.
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")