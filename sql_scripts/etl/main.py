from extract import extract_customers
from load import load_customers
from transform import transform_customers


def run_etl():
    df = extract_customers()
    df = transform_customers(df)
    load_customers(df)


if __name__ == "__main__":
    run_etl()
