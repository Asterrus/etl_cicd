CREATE SCHEMA dwh;

CREATE TABLE IF NOT EXISTS dwh.Customer_Dim (
    customer_sk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP NULL,
    is_current BOOLEAN NOT NULL,
    attr_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dwh.Product_Dim (
    product_sk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP NULL,
    is_current BOOLEAN NOT NULL,
    attr_hash TEXT NOT NULL
);

CREATE TABLE dwh.Sales_Fact(
    sale_sk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sale_id UUID NOT NULL,
    product_sk UUID REFERENCES dwh.Product_Dim(product_sk),
    customer_sk UUID REFERENCES dwh.Customer_Dim(customer_sk),
    sale_date TIMESTAMP NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dwh.data_quality_checks (
    id SERIAL PRIMARY KEY,
    check_name VARCHAR(100) NOT NULL,
    status VARCHAR(10) NOT NULL,
    value DECIMAL(10, 4),
    checked_at TIMESTAMP NOT NULL DEFAULT NOW()
);
