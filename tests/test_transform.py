def test_transform_customers():
    import pandas as pd

    from sql_scripts.etl.transform import transform_customers

    df = pd.DataFrame({"first_name": ["A"], "last_name": ["B"]})
    out = transform_customers(df)
    assert out["full_name"][0] == "A B"
