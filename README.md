## ETL Pipeline: Учётные системы → Хранилище данных

ETL-пайплайн на Airflow: перенос данных из OLTP-источника в DWH с проверками качества данных и мониторингом в Grafana.

### Архитектура

```mermaid
flowchart LR
    GEN[data-generator\nFaker + faker-commerce]

    subgraph source["OLTP (source)"]
        C[Customers]
        P[Products]
        S[Sales]
    end

    subgraph airflow["Airflow (CeleryExecutor) — каждую минуту"]
        ETL[run_etl]
        DQ[run_dq_checks]
        ETL --> DQ
    end

    subgraph dwh["DWH (dwh)"]
        CD[Customer_Dim\nSCD Type 2]
        PD[Product_Dim\nSCD Type 2]
        SF[Sales_Fact]
        DQT[data_quality_checks]
    end

    GEN --> source
    source --> ETL
    ETL --> CD
    ETL --> PD
    ETL --> SF
    DQ --> DQT
    DQT --> Grafana
```

### Инструменты

- Docker + docker-compose
- PostgreSQL 18
- Airflow 2.10.5 (CeleryExecutor + Redis)
- Python 3.13, uv
- Grafana (мониторинг качества данных)
- Faker + faker-commerce (генерация тестовых данных)

### Быстрый старт

1. Клонировать репозиторий:

   ```bash
   git clone ...
   cd etl_cicd
   ```

2. Создать `.env`:

   ```bash
   cp .env.example .env
   ```

3. Проверить `AIRFLOW_UID` (Linux — должен совпадать с `id -u`):

   ```bash
   echo "AIRFLOW_UID=$(id -u)" >> .env
   ```

4. Запустить окружение:

   ```bash
   make airflow-up
   ```

При первом запуске автоматически создаются схемы и загружаются начальные данные (5 клиентов, 5 продуктов, 8 продаж). После этого `data-generator` начинает непрерывно добавлять новые записи.

### Мониторинг

| Сервис | URL | Логин / пароль |
|--------|-----|----------------|
| Airflow UI | http://localhost:8080 | `airflow` / `airflow` |
| Grafana | http://localhost:3000 | `admin` / `admin` |

**Запуск DAG:**
1. Открыть Airflow UI → DAGs
2. Активировать:
   - `etl_dwh_prod` — запускается автоматически каждую минуту
   - `etl_dwh_test` — запуск вручную

Каждый DAG выполняет два шага: `run_etl → run_dq_checks`.

**Grafana — дашборд ETL Data Quality:**
- **Data Freshness** — часов с момента последней загрузки (порог: 24 ч)
- **Latest Check Status** — последние результаты проверок (OK / FAIL)
- **Source Tables (OLTP)** — текущее количество строк в Customers, Products, Sales
- **DWH Tables** — текущее количество строк в Customer_Dim, Product_Dim, Sales_Fact

### Генератор данных

Сервис `data-generator` автоматически наполняет `source`-таблицы случайными данными, чтобы дашборды Grafana показывали динамику.

Настройка через `.env`:

```env
GENERATOR_BATCH_SIZE=5    # записей за одну итерацию
GENERATOR_INTERVAL_SEC=30 # интервал между итерациями (секунды)
```

### Схема данных

```
data-generator ──► source.Customers  ──┐
                   source.Products   ──┼──► ETL ──► dwh.Customer_Dim (SCD2)
                   source.Sales      ──┘            dwh.Product_Dim  (SCD2)
                                                    dwh.Sales_Fact
                                                    dwh.data_quality_checks
```

Подробное описание полей: [docs/data_dictionary.md](docs/data_dictionary.md)

### Тестовое окружение

Тесты работают одновременно с запущенным Airflow (отдельный контейнер на порту 5433):

```bash
make test-up   # поднять тестовую БД
make test      # прогнать pytest
make test-down # остановить
```

### Проверка данных в БД

```bash
make psql-test   # подключиться к тестовой БД
make psql-prod   # подключиться к продуктовой БД
```

### Структура проекта

```
airflow/
  dags/etl_dag.py          # DAG: run_etl → run_dq_checks (prod — каждую минуту)
  Dockerfile
data_generator/
  main.py                  # цикл генерации: generate → insert → sleep
  db_connection.py
  scripts/
    data_generation.py     # Faker + faker-commerce
    insert_data.py         # INSERT в source.*
  Dockerfile
  pyproject.toml / uv.lock
docs/
  data_dictionary.md       # описание полей DWH-таблиц
entrypoints/
  db/                      # SQL-скрипты создания схем
  seed/seed.sql            # начальные данные
grafana/
  provisioning/            # автоматическая настройка datasource и дашборда
  dashboards/
src/
  sql_scripts/olap/        # ETL и DQ-логика
  sql_scripts/oltp.py      # хелперы для работы с источником
tests/                     # pytest
```

### Траблшутинг

**Контейнер не запускается**
```bash
docker compose -f docker-compose.airflow.yaml logs
```

**DAG не отображается в UI**
```bash
make check-dags
```

**Пересоздать окружение с нуля** (сбросить все данные)
```bash
make airflow-down
make airflow-up
```
