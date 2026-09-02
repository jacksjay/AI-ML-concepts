import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#load variables from .env
load_dotenv()

# SQLite file will be created automatically in this folder as patients.db
#SQLALCHEMY_DATABASE_URL = "sqlite:///./patients.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./patients.db")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only needed for SQLite
)

#SESSIONLOCAL: A factory that creates temporary database sessions (conversations).
# autocommit=False means we have to manually tell it to save changes using db.commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#The master class that all our database models will inherit from.
Base = declarative_base()

#DEPENDENCY INJECTION: A function used by FastAPI to give each web request its own DB session.
def get_db():
    """FastAPI dependency: yields a DB session and always closes it."""
    db = SessionLocal() # Open a new database conversation
    try:
        yield db # Hand the session over to the API endpoint
    finally:
        db.close() # close the connection when the endpoint finishes, even if it crashed
