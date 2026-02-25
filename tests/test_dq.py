from datetime import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.sql_scripts.olap.customer_dim import load_customer_dim
from src.sql_scripts.olap.data_quality import (
    run_completeness_check,
    run_data_quality_checks,
    run_freshness_check,
)
from src.sql_scripts.olap.etl import run_etl
from src.sql_scripts.oltp import insert_customer, insert_product, insert_sale


async def _get_last_check(session: AsyncSession, check_name: str):
    result = await session.execute(
        text(
            "SELECT status, value FROM dwh.data_quality_checks "
            "WHERE check_name = :name ORDER BY checked_at DESC LIMIT 1"
        ),
        {"name": check_name},
    )
    return result.fetchone()


class TestFreshnessCheck:
    """Тесты проверки свежести данных"""

    @pytest.mark.asyncio
    async def test_freshness_ok(self, session: AsyncSession):
        """Данные загружены только что → valid_from ≈ NOW() → OK, value близко к 0"""
        await insert_customer(session, name="Customer 1", email="c1@example.com", phone="1111")
        await load_customer_dim(session)

        await run_freshness_check(session)

        row = await _get_last_check(session, "freshness")
        assert row
        assert row.status == "OK"
        assert row.value is not None
        assert row.value < 24

    @pytest.mark.asyncio
    async def test_freshness_fail_empty_dim(self, session: AsyncSession):
        """Customer_Dim пустой → MAX(valid_from) = NULL → FAIL, value = NULL"""
        await run_freshness_check(session)

        row = await _get_last_check(session, "freshness")
        assert row
        assert row.status == "FAIL"
        assert row.value is None

    @pytest.mark.asyncio
    async def test_freshness_fail_stale_data(self, session: AsyncSession):
        """Последняя запись в Customer_Dim была 25 часов назад → данные устарели → FAIL"""
        await session.execute(text("""
            INSERT INTO dwh.Customer_Dim
                (customer_id, name, email, phone, valid_from, valid_to, is_current, attr_hash)
            VALUES
                (gen_random_uuid(), 'Old Customer', 'old@example.com', '0000',
                 NOW() - interval '25 hours', NULL, TRUE, 'hash')
        """))

        await run_freshness_check(session)

        row = await _get_last_check(session, "freshness")
        assert row
        assert row.status == "FAIL"
        assert row.value > 24


class TestCompletenessCheck:
    """Тесты проверки полноты данных"""

    @pytest.mark.asyncio
    async def test_completeness_ok_equal_counts(self, session: AsyncSession):
        """source.Sales и dwh.Sales_Fact совпадают → расхождение 0% → OK, value = 0"""
        customer_id = await insert_customer(
            session, name="Customer 1", email="c1@example.com", phone="1111"
        )
        product_id = await insert_product(session, "Product 1", "Category 1")
        await insert_sale(
            session,
            customer_id=customer_id,
            product_id=product_id,
            sale_date=datetime.now(),
            amount=100.0,
            quantity=1,
        )
        await run_etl(session)

        await run_completeness_check(session)

        row = await _get_last_check(session, "completeness")
        assert row
        assert row.status == "OK"
        assert row.value == 0

    @pytest.mark.asyncio
    async def test_completeness_fail_empty_source(self, session: AsyncSession):
        """source.Sales пустой → аномалия → FAIL, value = 1"""
        await run_completeness_check(session)

        row = await _get_last_check(session, "completeness")
        assert row
        assert row.status == "FAIL"
        assert row.value == 1

    @pytest.mark.asyncio
    async def test_completeness_fail_missing_records(self, session: AsyncSession):
        """В source есть продажи, ETL не запускался → DWH пустой → FAIL, value = 1"""
        customer_id = await insert_customer(
            session, name="Customer 1", email="c1@example.com", phone="1111"
        )
        product_id = await insert_product(session, "Product 1", "Category 1")
        await insert_sale(
            session,
            customer_id=customer_id,
            product_id=product_id,
            sale_date=datetime.now(),
            amount=100.0,
            quantity=1,
        )
        # ETL намеренно не запускаем — dwh.Sales_Fact остаётся пустым

        await run_completeness_check(session)

        row = await _get_last_check(session, "completeness")
        assert row
        assert row.status == "FAIL"
        assert row.value == 1


class TestRunDataQualityChecks:
    """Тесты запуска всех проверок разом"""

    @pytest.mark.asyncio
    async def test_writes_both_checks(self, session: AsyncSession):
        """run_data_quality_checks записывает ровно 2 строки: freshness и completeness"""
        await run_data_quality_checks(session)

        result = await session.execute(
            text("SELECT check_name FROM dwh.data_quality_checks ORDER BY check_name")
        )
        rows = result.fetchall()
        check_names = {r.check_name for r in rows}

        assert len(rows) == 2
        assert "freshness" in check_names
        assert "completeness" in check_names
