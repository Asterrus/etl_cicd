import sys

# Гарантируем, что subprocess'ы LocalExecutor видят твои модули
for path in ["/opt/src", "/opt/airflow/dags"]:
    if path not in sys.path:
        sys.path.insert(0, path)
