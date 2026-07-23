"""Database engine and session configuration."""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL,echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    )

Base = declarative_base()


#dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()