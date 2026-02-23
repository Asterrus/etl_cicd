CREATE SCHEMA source;

CREATE TABLE IF NOT EXISTS source.Customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS source.Products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS source.Sales (
    sale_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES source.Customers(customer_id),
    product_id UUID NOT NULL REFERENCES source.Products(product_id),
    sale_date TIMESTAMP NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL
);