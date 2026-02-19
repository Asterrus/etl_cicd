import pandas as pd


def extract_customers(con) -> pd.DataFrame:
    return pd.read_sql("SELECT * FROM source.customers", con)
