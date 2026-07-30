import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file.")

class Base(DeclarativeBase): 
    pass

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def test_database_connection() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        
def create_database():
    Base.metadata.create_all(bind=engine)
    
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()