import logging

from sqlalchemy.ext.asyncio import AsyncSession

from .customer_dim import load_customer_dim
from .product_dim import load_product_dim
from .sales_fact import load_sales_fact

logger = logging.getLogger(__name__)


async def run_etl(session: AsyncSession):
    logger.info("Starting ETL process")
    await load_customer_dim(session)
    await load_product_dim(session)
    await load_sales_fact(session)
    logger.info("ETL process completed")
