"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Base per i modelli
Base = declarative_base()

# Path del database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "phantom_thieves.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Engine e session factory
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with all tables."""
    from models.user import User
    from models.task import Task
    from models.palace import Palace
    
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized at: {DB_PATH}")


if __name__ == "__main__":
    init_db()

