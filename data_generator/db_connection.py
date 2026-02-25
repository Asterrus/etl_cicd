import os

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def get_database_url() -> str:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", "5432")
    assert all([user, password, db, host, port]), "Missing required database environment variables"
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"


def create_engine(url: str) -> AsyncEngine:
    return create_async_engine(url)
