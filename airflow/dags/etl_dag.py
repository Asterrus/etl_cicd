from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pprint import pprint

import pendulum
from airflow.providers.standard.operators.python import (
    PythonOperator,
)
from airflow.sdk import dag, task
from sqlalchemy.ext.asyncio import async_sessionmaker

from airflow import DAG
from db.engine import create_engine
from sql_scripts.olap.etl import run_etl

logger = logging.getLogger(__name__)


# def _build_test_db_url() -> str:
#     postgres_user = os.getenv("POSTGRES_TEST_USER", "etl_test")
#     postgres_password = os.getenv("POSTGRES_TEST_PASSWORD", "etl_test_password")
#     postgres_db = os.getenv("POSTGRES_TEST_DB", "etl_test")
#     postgres_host = os.getenv("POSTGRES_TEST_HOST", "db_test")
#     postgres_port = os.getenv("POSTGRES_TEST_PORT", "5432")
#     return f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


# def _build_prod_db_url() -> str:
#     postgres_user = os.getenv("POSTGRES_PROD_USER", "etl_prod")
#     postgres_password = os.getenv("POSTGRES_PROD_PASSWORD", "etl_prod_password")
#     postgres_db = os.getenv("POSTGRES_PROD_DB", "etl_prod")
#     postgres_host = os.getenv("POSTGRES_PROD_HOST", "db_prod")
#     postgres_port = os.getenv("POSTGRES_PROD_PORT", "5432")
#     return f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


# async def _run_etl_for_url(db_url: str) -> None:
#     engine = create_engine(db_url, is_echo=False)
#     session_factory = async_sessionmaker(engine, expire_on_commit=False)

#     async with session_factory() as session:
#         await run_etl(session)


# def run_etl_test() -> None:
#     db_url = _build_test_db_url()
#     asyncio.run(_run_etl_for_url(db_url))


# def run_etl_prod() -> None:
#     db_url = _build_prod_db_url()
#     asyncio.run(_run_etl_for_url(db_url))


# default_args = {
#     "owner": "etl",
#     "start_date": datetime(2025, 1, 1),
# }


# with DAG(
#     dag_id="etl_dwh_prod",
#     default_args=default_args,
#     schedule=None,
#     catchup=False,
#     tags=["etl", "dwh", "prod"],
# ) as dag_prod:
#     run_etl_prod_task = PythonOperator(
#         task_id="run_etl_prod",
#         python_callable=run_etl_prod,
#     )


# dag_test = DAG(
#     dag_id="etl_dwh_test",
#     default_args=default_args,
#     schedule=None,
#     catchup=False,
#     tags=["etl", "dwh", "test"],
# )

# PythonOperator(
#     task_id="run_etl_test",
#     python_callable=run_etl_test,
#     dag=dag_test,
# )


# # Делаем функцию async и убираем asyncio.run()
# async def run_etl_test():
#     logger.info(">>> ETL STARTED")
#     logger.debug(">>> ETL STARTED")
#     try:
#         logger.info(">>> ETL STARTED")
#         logger.debug(">>> ETL STARTED")
#         db_url = _build_test_db_url()
#         logger.info(f">>> DB URL: {db_url}")
#         logger.debug(f">>> DB URL: {db_url}")
#         await _run_etl_for_url(db_url)
#     except Exception as e:
#         logger.error(f">>> ERROR: {e}")
#         import traceback

#         traceback.print_exc(file=sys.stderr)
#         raise  # пусть Airflow увидит failure
#     # db_url = _build_test_db_url()
#     # await _run_etl_for_url(db_url)


# # В DAG оставляем обычный PythonOperator
# PythonOperator(
#     task_id="run_etl_test",
#     python_callable=run_etl_test,  # Airflow 3.x сам detect-ит async
#     dag=dag_test,
# )


# async def async_task():
#     logger.info("ASYNC TASK STARTED")  # Это должно попасть в лог
#     await asyncio.sleep(1)
#     logger.info("ASYNC TASK COMPLETED")


# with DAG(
#     "debug_async",
#     start_date=datetime(2025, 1, 1),
#     schedule=None,
#     catchup=False,
#     tags=["debug"],
# ) as dag:
#     PythonOperator(task_id="async_task", python_callable=async_task)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def tutorial_taskflow_api():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """

    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        order_data_dict = json.loads(data_string)
        return order_data_dict

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        """
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """

        print(f"Total order value is: {total_order_value:.2f}")

    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])


tutorial_taskflow_api()
