from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def run_freshness_check(session: AsyncSession):
    # Свежесть: сколько часов прошло с последней загрузки.
    await session.execute(
        text("""
        WITH last_load AS (
            SELECT EXTRACT(EPOCH FROM (NOW() - MAX(valid_from))) / 3600 AS hours
            FROM dwh.Customer_Dim
        )
        INSERT INTO dwh.data_quality_checks (check_name, status, value)
        SELECT
            'freshness',
            CASE WHEN hours < 24 THEN 'OK' ELSE 'FAIL' END,
            ROUND(hours::numeric, 4)
        FROM last_load
    """)
    )


async def run_completeness_check(session: AsyncSession) -> None:
    # Полнота: ABS(source - dwh) / source.
    await session.execute(
        text("""
        WITH counts AS (
            SELECT
                (SELECT COUNT(*) FROM source.Sales)   AS source_count,
                (SELECT COUNT(*) FROM dwh.Sales_Fact) AS dwh_count
        )
        INSERT INTO dwh.data_quality_checks (check_name, status, value)
        SELECT
            'completeness',
            CASE
                WHEN source_count = 0 THEN 'FAIL'
                WHEN ABS(source_count - dwh_count)::float / source_count <= 0.05 THEN 'OK'
                ELSE 'FAIL'
            END,
            ROUND(
                CASE WHEN source_count = 0 THEN 1.0
                     ELSE ABS(source_count - dwh_count)::numeric / source_count
                END, 4
            )
        FROM counts
    """)
    )


async def run_data_quality_checks(session: AsyncSession) -> None:
    await run_freshness_check(session)
    await run_completeness_check(session)
