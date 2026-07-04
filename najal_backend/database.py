"""
najal_backend/database.py
----------------------------
إعداد الاتصال بقاعدة البيانات عبر SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./najal.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency لـ FastAPI — يفتح جلسة ويقفلها تلقائياً بعد كل طلب."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        """ hh"""