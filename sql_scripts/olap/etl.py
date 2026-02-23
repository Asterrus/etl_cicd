from sqlalchemy.ext.asyncio import AsyncSession

from sql_scripts.olap.customer_dim import load_customer_dim
from sql_scripts.olap.product_dim import load_product_dim
from sql_scripts.olap.sales_fact import load_sales_fact


async def run_etl(session: AsyncSession):
    await load_customer_dim(session)
    await load_product_dim(session)
    await load_sales_fact(session)
