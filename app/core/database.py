"""Database configuration and session helpers."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# PERUBAHAN PENTING: Import NullPool
from sqlalchemy.pool import NullPool

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=False,
    # PERUBAHAN PENTING: Pakai NullPool untuk Vercel (Serverless)
    poolclass=NullPool,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()