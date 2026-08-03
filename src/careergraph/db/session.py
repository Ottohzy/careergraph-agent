from collections.abc import Generator
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///careergraph.db"  # Replace with your actual database URL

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})  # For SQLite, disable same-thread check
SessionLocal = sessionmaker(expire_on_commit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()