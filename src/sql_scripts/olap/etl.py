from sqlalchemy.ext.asyncio import AsyncSession

from .customer_dim import load_customer_dim
from .product_dim import load_product_dim
from .sales_fact import load_sales_fact


async def run_etl(session: AsyncSession):
    await load_customer_dim(session)
    await load_product_dim(session)
    await load_sales_fact(session)
