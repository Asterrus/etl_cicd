import logging
from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

logger = logging.getLogger(__name__)


def simple_python_task():
    logger.info("=== SIMPLE PYTHON TASK STARTED ===")
    result = 2 + 2
    logger.info(f"=== CALCULATION RESULT: {result} ===")
    logger.info("=== SIMPLE PYTHON TASK COMPLETED ===")
    return result


with DAG(
    dag_id="test_python_simple",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test", "python", "simple"],
) as dag:
    task = PythonOperator(
        task_id="simple_task",
        python_callable=simple_python_task,
    )
