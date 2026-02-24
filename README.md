### Описание

ETL-пайплайн: перенос данных из OLTP-источника в хранилище данных (DWH).

### Инструменты

- docker
- docker-compose
- PostgreSQL
- Airflow (CeleryExecutor)
- Python 3.13
- uv

### Запуск

1. Клонировать репозиторий и перейти в директорию проекта:

   ```bash
   git clone ...
   cd etl_cicd
   ```

2. Создать .env файл с переменными окружения:

   ```bash
   cp .env.example .env
   ```

3. Проверить что `AIRFLOW_UID` в .env совпадает с id текущего пользователя.
   Linux:
   ```bash
   id
   ```
   Mac/Windows: 50000 или убрать переменную.

4. Запустить Airflow со всеми зависимостями:

   ```bash
   make airflow-up
   ```

### Тестовые данные

При первом запуске контейнеры инициализируются автоматически: 5 клиентов, 5 продуктов, 8 продаж.

Путь к файлу с тестовыми данными: entrypoints/seed/seed.sql  
Путь к скриптам создания таблиц: entrypoints/db/create_tables.sql  
Airflow DAGs: airflow/dags/etl_dag.py  
ETL скрипты: src/sql_scripts/

### Проверка работы

1. Открыть Airflow UI: http://127.0.0.1:8080
   Логин/пароль: `airflow` / `airflow`

2. Активировать и запустить нужный DAG:
   - `etl_dwh_test` — тестовое окружение
   - `etl_dwh_prod` — продуктовое окружение

3. Проверить данные в БД:

   ```bash
   make psql-test   # подключиться к тестовой БД
   make psql-prod   # подключиться к продуктовой БД
   ```

### Тестовое окружение

Запустить тесты отдельно от Airflow:

```bash
make test-up   # поднять тестовую БД
make test      # прогнать pytest
make test-down # остановить
```
