.PHONY: init up down retrieve load-clickhouse migrate-postgres reset
init:
	poetry install
up:
	docker-compose up -d
down:
	docker-compose down
retrieve:
	PYTHONPATH=. poetry run python scripts/retrieve_data.py
load-clickhouse:
	PYTHONPATH=. poetry run python scripts/load_clickhouse.py
migrate-postgres:
	PYTHONPATH=. poetry run python scripts/migrate_to_postgres.py
extract-csvs:
	PYTHONPATH=. poetry run python scripts/extract_csvs.py
analyze-columns:
	PYTHONPATH=. poetry run python scripts/analyze_columns.py
query-databases:
	PYTHONPATH=. poetry run python scripts/query_databases.py
migrate-clickhouse-to-postgres:
	PYTHONPATH=. poetry run python scripts/migrate_clickhouse_to_postgres.py
reset:
	docker-compose down -v