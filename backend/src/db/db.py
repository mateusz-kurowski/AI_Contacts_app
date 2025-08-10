import os
import time

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def wait_for_db(max_retries=30, delay=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                print("Database connection established!")
                return True
        except OperationalError as e:
            print(f"Database not ready, attempt {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise Exception("Could not connect to database after multiple attempts")
    return False


def create_tables():
    """Create all tables in the database"""
    try:
        wait_for_db()

        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
