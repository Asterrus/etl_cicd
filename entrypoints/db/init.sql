CREATE SCHEMA source;
CREATE SCHEMA dwh;

CREATE TABLE IF NOT EXISTS source.Customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS source.Category (
    category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS source.Products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_name VARCHAR(255) NOT NULL,
    category_id UUID NOT NULL REFERENCES Category(category_id),
);

CREATE TABLE IF NOT EXISTS source.Orders (
    order_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id  UUID NOT NULL REFERENCES Customers(customer_id),
    order_date   TIMESTAMP NOT NULL DEFAULT NOW(),
    status       VARCHAR(50) NOT NULL DEFAULT 'new',          -- new, paid, shipped, delivered, cancelled...
    payment_method VARCHAR(50),
    shipping_address TEXT,
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS source.OrderItem (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id      UUID NOT NULL REFERENCES Orders(order_id) ON DELETE CASCADE,
    product_id    UUID NOT NULL REFERENCES Products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    DECIMAL(10,2) NOT NULL,
    amount        DECIMAL(12,2) GENERATED ALWAYS AS (quantity * unit_price)
);
