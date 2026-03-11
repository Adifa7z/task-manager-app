from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Read the database URL from environment variables (set in docker-compose.yml)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/taskdb"
)

# Create the database engine (the connection)
engine = create_engine(DATABASE_URL)

# Each request gets its own session (like a conversation with the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all our database models will inherit from
Base = declarative_base()

# Dependency — gives a DB session to each API route, then closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()