import asyncio
import logging
from datetime import datetime

from airflow.providers.standard.operators.python import PythonOperator

from airflow import DAG

logger = logging.getLogger(__name__)


async def async_task_impl():
    logger.info("=== ASYNC TASK STARTED ===")
    await asyncio.sleep(1)
    logger.info("=== ASYNC TASK COMPLETED AFTER SLEEP ===")
    return "async_result"


def async_task():
    return asyncio.run(async_task_impl())


def async_task():
    return asyncio.run(async_task_impl())


with DAG(
    dag_id="test_python_async",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test", "python", "async"],
) as dag:
    task = PythonOperator(
        task_id="async_task",
        python_callable=async_task,
    )
