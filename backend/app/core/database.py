"""Database engine and session configuration."""

from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from sqlalchemy import create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL,echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    )

#dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


