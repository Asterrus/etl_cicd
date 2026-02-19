from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from sql_scripts.etl.main import run_etl

with DAG("etl_demo", start_date=datetime(2024, 1, 1), schedule="@daily") as dag:
    etl = PythonOperator(task_id="run_etl", python_callable=run_etl)
