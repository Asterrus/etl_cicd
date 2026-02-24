INSERT INTO source.Customers (name, email, phone) VALUES
    ('Иван Петров',    'ivan.petrov@example.com',    '+7-900-111-2233'),
    ('Мария Сидорова', 'maria.sidorova@example.com', '+7-900-222-3344'),
    ('Алексей Козлов', 'alexey.kozlov@example.com',  '+7-900-333-4455'),
    ('Ольга Новикова', 'olga.novikova@example.com',  '+7-900-444-5566'),
    ('Дмитрий Волков', 'dmitry.volkov@example.com',  '+7-900-555-6677');

INSERT INTO source.Products (product_name, category) VALUES
    ('Ноутбук Lenovo ThinkPad',  'Электроника'),
    ('Смартфон Samsung Galaxy',  'Электроника'),
    ('Наушники Sony WH-1000XM5', 'Электроника'),
    ('Офисное кресло',           'Мебель'),
    ('Механическая клавиатура',  'Периферия');

INSERT INTO source.Sales (customer_id, product_id, sale_date, amount, quantity)
SELECT c.customer_id, p.product_id, s.sale_date, s.amount, s.quantity
FROM (VALUES
    ('ivan.petrov@example.com',    'Ноутбук Lenovo ThinkPad',  '2025-01-05 10:00:00'::timestamp, 85000.00, 1),
    ('ivan.petrov@example.com',    'Механическая клавиатура',  '2025-01-05 10:15:00'::timestamp,  7500.00, 1),
    ('maria.sidorova@example.com', 'Смартфон Samsung Galaxy',  '2025-01-10 14:30:00'::timestamp, 62000.00, 2),
    ('alexey.kozlov@example.com',  'Наушники Sony WH-1000XM5', '2025-01-12 09:00:00'::timestamp, 28000.00, 1),
    ('alexey.kozlov@example.com',  'Офисное кресло',           '2025-01-15 11:00:00'::timestamp, 18500.00, 2),
    ('olga.novikova@example.com',  'Ноутбук Lenovo ThinkPad',  '2025-01-18 16:00:00'::timestamp, 85000.00, 1),
    ('dmitry.volkov@example.com',  'Смартфон Samsung Galaxy',  '2025-01-20 12:00:00'::timestamp, 62000.00, 1),
    ('dmitry.volkov@example.com',  'Механическая клавиатура',  '2025-01-20 12:30:00'::timestamp,  7500.00, 3)
) AS s(email, product_name, sale_date, amount, quantity)
JOIN source.Customers c ON c.email = s.email
JOIN source.Products  p ON p.product_name = s.product_name;
