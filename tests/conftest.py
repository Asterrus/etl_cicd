import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import Session as SyncSession
from sqlalchemy.orm.session import SessionTransaction

from src.db.engine import create_engine

load_dotenv()


def get_database_url() -> str:
    if url := os.getenv("TEST_DATABASE_URL"):
        return url
    postgres_user = os.getenv("POSTGRES_TEST_USER", "etl_test")
    postgres_password = os.getenv("POSTGRES_TEST_PASSWORD", "etl_test_password")
    postgres_db = os.getenv("POSTGRES_TEST_DB", "etl_test")
    postgres_host = os.getenv("POSTGRES_LOCAL_TEST_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_TEST_PORT", "5432")
    return f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


@pytest.fixture(scope="session")
def engine():
    url = get_database_url()
    return create_engine(url, is_echo=True)


async_session_factory = async_sessionmaker(engine, expire_on_commit=False)  # type: ignore


@pytest_asyncio.fixture
async def session(engine: AsyncEngine):
    async with engine.connect() as conn:
        trans = await conn.begin()

        Session = async_session_factory

        async with Session(bind=conn) as s:
            await s.begin_nested()

            @event.listens_for(s.sync_session, "after_transaction_end")
            def restart_savepoint(
                sync_sess: SyncSession, transaction: SessionTransaction
            ):
                if not transaction.nested:
                    return
                if sync_sess.is_active and sync_sess.get_transaction() is not None:
                    return
                sync_sess.begin_nested()

            try:
                yield s
            finally:
                await trans.rollback()
