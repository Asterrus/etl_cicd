import random
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def insert_batch(engine: AsyncEngine, customers: list[dict], products: list[dict]) -> None:
    async with engine.begin() as conn:
        customer_ids = []
        for customer in customers:
            result = await conn.execute(
                text(
                    "INSERT INTO source.Customers (name, email, phone) "
                    "VALUES (:name, :email, :phone) RETURNING customer_id"
                ),
                customer,
            )
            customer_ids.append(result.scalar_one())

        product_ids = []
        for product in products:
            result = await conn.execute(
                text(
                    "INSERT INTO source.Products (product_name, category) "
                    "VALUES (:product_name, :category) RETURNING product_id"
                ),
                product,
            )
            product_ids.append(result.scalar_one())

        for customer_id in customer_ids:
            await conn.execute(
                text(
                    "INSERT INTO source.Sales (customer_id, product_id, sale_date, amount, quantity) "
                    "VALUES (:customer_id, :product_id, :sale_date, :amount, :quantity)"
                ),
                {
                    "customer_id": str(customer_id),
                    "product_id": str(random.choice(product_ids)),
                    "sale_date": datetime.now(),
                    "amount": round(random.uniform(500, 50000), 2),
                    "quantity": random.randint(1, 10),
                },
            )
