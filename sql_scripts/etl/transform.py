import pandas as pd


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df["full_name"] = df["first_name"] + " " + df["last_name"]
    return df
