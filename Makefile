.PHONY: up down test-up test-down

up:
	docker compose up -d --build

down:
	docker compose down --volumes --remove-orphans

test-up:
	docker compose -f docker-compose.test.yaml up -d --build

test-down:
	docker compose -f docker-compose.test.yaml down --volumes --remove-orphans

test:
	uv run pytest tests