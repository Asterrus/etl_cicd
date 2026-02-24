.PHONY: up down prod-up prod-down test-up test-down airflow-up airflow-down check-dags run-simple run-async run-etl

up:
	docker compose up -d --build

down:
	docker compose down --volumes --remove-orphans

prod-up:
	docker compose up -d --build

prod-down:
	docker compose down --volumes --remove-orphans

test-up:
	docker compose -f docker-compose.test.yaml up -d --build

test-down:
	docker compose -f docker-compose.test.yaml down --volumes --remove-orphans

test:
	uv run pytest tests

airflow-up:
	docker compose -f docker-compose.airflow.yaml up -d --build

airflow-down:
	docker compose -f docker-compose.airflow.yaml down --volumes --remove-orphans

check-dags:
	docker compose -f docker-compose.airflow.yaml exec airflow-webserver airflow dags list
	docker compose -f docker-compose.airflow.yaml exec airflow-webserver airflow dags list-import-errors
	docker compose -f docker-compose.airflow.yaml exec airflow-webserver python -c "import etl_dag"

run-simple:
	docker compose -f docker-compose.airflow.yaml exec airflow-scheduler airflow tasks test test_python_simple simple_task 2025-01-01

run-async:
	docker compose -f docker-compose.airflow.yaml exec airflow-scheduler airflow tasks test test_python_async async_task 2025-01-01

run-etl:
	docker compose -f docker-compose.airflow.yaml exec airflow-scheduler airflow tasks test etl_dwh_test run_etl_test 2025-01-01