from __future__ import annotations

import asyncio
import logging
import os
from datetime import datetime

from airflow.operators.python import PythonOperator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from airflow import DAG
from db.engine import create_engine
from sql_scripts.olap.etl import run_etl

logger = logging.getLogger(__name__)


def _build_test_db_url() -> str:
    postgres_user = os.getenv("POSTGRES_TEST_USER", "etl_test")
    postgres_password = os.getenv("POSTGRES_TEST_PASSWORD", "etl_test_password")
    postgres_db = os.getenv("POSTGRES_TEST_DB", "etl_test")
    postgres_host = os.getenv("POSTGRES_TEST_HOST", "etl-cicd-db-test")
    postgres_port = os.getenv("POSTGRES_TEST_PORT", "5432")
    return f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


def _build_prod_db_url() -> str:
    postgres_user = os.getenv("POSTGRES_PROD_USER", "etl_prod")
    postgres_password = os.getenv("POSTGRES_PROD_PASSWORD", "etl_prod_password")
    postgres_db = os.getenv("POSTGRES_PROD_DB", "etl_prod")
    postgres_host = os.getenv("POSTGRES_PROD_HOST", "etl-cicd-db-prod")
    postgres_port = os.getenv("POSTGRES_PROD_PORT", "5434")
    return f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


async def _run_etl_for_url(db_url: str) -> None:
    engine = create_engine(db_url, is_echo=False)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        await run_etl(session)


def run_etl_test() -> None:
    db_url = _build_test_db_url()
    asyncio.run(_run_etl_for_url(db_url))


def run_etl_prod() -> None:
    db_url = _build_prod_db_url()
    asyncio.run(_run_etl_for_url(db_url))


default_args = {
    "owner": "etl",
    "start_date": datetime(2025, 1, 1),
}


with DAG(
    dag_id="etl_dwh_test",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["etl", "dwh", "test"],
) as dag_test:
    run_etl_test_task = PythonOperator(
        task_id="run_etl_test",
        python_callable=run_etl_test,
    )

with DAG(
    dag_id="etl_dwh_prod",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["etl", "dwh", "prod"],
) as dag_prod:
    run_etl_prod_task = PythonOperator(
        task_id="run_etl_prod",
        python_callable=run_etl_prod,
    )
