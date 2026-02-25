import faker_commerce
from faker import Faker

fake = Faker("ru_RU")
fake.add_provider(faker_commerce.Provider)


def generate_customer() -> dict:
    return {
        "name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
    }


def generate_product() -> dict:
    return {
        "product_name": fake.ecommerce_name(),
        "category": fake.ecommerce_category(),
    }


def generate_batch(batch_size: int) -> tuple[list[dict], list[dict]]:
    customers = [generate_customer() for _ in range(batch_size)]
    products = [generate_product() for _ in range(batch_size)]
    return customers, products
