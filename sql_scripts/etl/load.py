import pandas as pd


def load_customers(df: pd.DataFrame, con):
    df.to_sql("dim_customers", con, if_exists="replace")
