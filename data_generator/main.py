import asyncio
import logging
import os

from db_connection import create_engine, get_database_url
from dotenv import load_dotenv
from scripts.data_generation import generate_batch
from scripts.insert_data import insert_batch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


async def main():
    batch_size = int(os.environ.get("GENERATOR_BATCH_SIZE", 5))
    interval = int(os.environ.get("GENERATOR_INTERVAL_SEC", 30))

    logger.info("Starting data generator")
    logger.info(f"Batch size: {batch_size}, interval: {interval}s")

    engine = create_engine(get_database_url())

    while True:
        customers, products = generate_batch(batch_size)
        await insert_batch(engine, customers, products)
        logger.info(f"Inserted {batch_size} customers, {batch_size} products, {batch_size} sales")
        await asyncio.sleep(interval)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Generator stopped")
