-include .env
export

POSTGRES_TEST_USER ?= etl_test
POSTGRES_TEST_DB   ?= etl_test
POSTGRES_PROD_USER ?= etl_prod
POSTGRES_PROD_DB   ?= etl_prod

.PHONY: prod-up prod-down test-up test-down test airflow-up airflow-down check-dags run-etl psql-test psql-prod

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

run-etl:
	docker compose -f docker-compose.airflow.yaml exec airflow-scheduler airflow tasks test etl_dwh_test run_etl_test 2025-01-01

psql-test:
	docker compose -f docker-compose.airflow.yaml exec -it db_test psql -U $(POSTGRES_TEST_USER) -d $(POSTGRES_TEST_DB)

psql-prod:
	docker compose -f docker-compose.airflow.yaml exec -it db_prod psql -U $(POSTGRES_PROD_USER) -d $(POSTGRES_PROD_DB)
