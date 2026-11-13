IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'dim')
BEGIN
    EXEC('CREATE SCHEMA dim');
END
GO

IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = 'fact')
BEGIN
    EXEC('CREATE SCHEMA fact');
END
GO

IF Object_ID('dim.products', 'U') IS NOT NULL
    DROP TABLE dim.products;
CREATE TABLE dim.products(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL);

IF Object_ID('dim.customers', 'U') IS NOT NULL
    DROP TABLE dim.customers;   
    create table dim.customers(
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL);

IF Object_ID('dim.store', 'U') IS NOT NULL
    DROP TABLE dim.store;   
    create table dim.store(
    store_id INT PRIMARY KEY,
    store_name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL);

IF Object_ID('dim.Date', 'U') IS NOT NULL
    DROP TABLE dim.Date;   
    create table dim.Date(
    date_id INT PRIMARY KEY,
    date_value DATE NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    month VARCHAR(20) NOT NULL,
    year INT NOT NULL);

IF Object_ID('fact.sales', 'U') IS NOT NULL
    DROP TABLE fact.sales;
    create table fact.sales(
    sales_id INT PRIMARY KEY,
    product_id INT NOT NULL REFERENCES dim.products(product_id),
    customer_id INT NOT NULL REFERENCES dim.customers(customer_id),
    store_id INT NOT NULL REFERENCES dim.store(store_id),
    date_id INT NOT NULL REFERENCES dim.Date(date_id),
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL
    );

--inserting the values

-- 1. INSERT PRODUCTS

INSERT INTO dim.products
    (product_id, product_name, category, brand)
VALUES
    (1, 'Laptop', 'Electronics', 'Dell'),
    (2, 'Mouse', 'Accessories', 'Logitech'),
    (3, 'Keyboard', 'Accessories', 'HP'),
    (4, 'Monitor', 'Electronics', 'Samsung'),
    (5, 'Smartphone', 'Electronics', 'Apple'),
    (6, 'Headphones', 'Accessories', 'Sony'),
    (7, 'Office Chair', 'Furniture', 'IKEA'),
    (8, 'USB Hub', 'Accessories', 'Anker');


-- 2. INSERT CUSTOMERS

INSERT INTO dim.customers
    (customer_id, customer_name, gender, age)
VALUES
    (101, 'Ali', 'Male', 25),
    (102, 'Anees', 'Male', 30),
    (103, 'Ayesha', 'Female', 27),
    (104, 'Sara', 'Female', 32),
    (105, 'Lubaba', 'Male', 28),
    (106, 'Hassan', 'Male', 35),
    (107, 'Fatima', 'Female', 24),
    (108, 'Zain', 'Male', 29);


-- 3. INSERT STORES

INSERT INTO dim.store
    (store_id, store_name, location)
VALUES
    (201, 'Main Store', 'Lahore'),
    (202, 'City Store', 'Karachi'),
    (203, 'Online Store', 'Online'),
    (204, 'North Store', 'Peshawar');


-- 4. INSERT DATES

INSERT INTO dim.[Date]
    (date_id, date_value, day_of_week, month, year)
VALUES
    (20261101, '2026-11-01', 'Sunday', 'November', 2026),
    (20261102, '2026-11-02', 'Monday', 'November', 2026),
    (20261103, '2026-11-03', 'Tuesday', 'November', 2026),
    (20261104, '2026-11-04', 'Wednesday', 'November', 2026),
    (20261105, '2026-11-05', 'Thursday', 'November', 2026),
    (20261106, '2026-11-06', 'Friday', 'November', 2026),
    (20261107, '2026-11-07', 'Saturday', 'November', 2026),
    (20261108, '2026-11-08', 'Sunday', 'November', 2026);


-- 5. INSERT SALES FACTS

INSERT INTO fact.sales
    (sales_id, product_id, customer_id, store_id,
     date_id, price, quantity, total_amount)
VALUES
    (5001, 1, 101, 201, 20261101, 1200.00, 1, 1200.00),
    (5002, 2, 102, 203, 20261101,   25.00, 2,   50.00),
    (5003, 3, 103, 202, 20261102,   75.00, 1,   75.00),
    (5004, 4, 101, 201, 20261102,  350.00, 2,  700.00),
    (5005, 5, 104, 203, 20261103,  950.00, 1,  950.00),
    (5006, 6, 105, 204, 20261103,  150.00, 2,  300.00),
    (5007, 7, 106, 201, 20261104,  200.00, 1,  200.00),
    (5008, 8, 102, 202, 20261104,   45.00, 3,  135.00),
    (5009, 2, 107, 203, 20261105,   25.00, 4,  100.00),
    (5010, 1, 103, 202, 20261105, 1200.00, 1, 1200.00),
    (5011, 4, 108, 204, 20261106,  350.00, 1,  350.00),
    (5012, 3, 105, 203, 20261106,   75.00, 2,  150.00),
    (5013, 5, 101, 201, 20261107,  950.00, 1,  950.00),
    (5014, 7, 107, 202, 20261107,  200.00, 2,  400.00),
    (5015, 6, 104, 203, 20261108,  150.00, 1,  150.00),
    (5016, 8, 106, 201, 20261108,   45.00, 2,   90.00),
    (5017, 1, 102, 203, 20261108, 1200.00, 1, 1200.00),
    (5018, 2, 108, 204, 20261107,   25.00, 3,   75.00),
    (5019, 4, 105, 202, 20261106,  350.00, 2,  700.00),
    (5020, 5, 103, 201, 20261105,  950.00, 1,  950.00);

--checking out the table contents
select * from dim.products;
select * from dim.customers;
select * from dim.store;
select * from dim.[Date];
select * from fact.sales;

--Table creation and data insertion script for star schema done
--desiging the star schema for now 
select c.customer_id,c.customer_name,p.product_id,p.product_name,
       p.category,s.store_id,s.store_name, f.quantity,f.total_amount
 FROM fact.sales AS f
    INNER JOIN dim.customers AS c ON f.customer_id = c.customer_id
    INNER JOIN dim.products AS p ON f.product_id = p.product_id
    INNER JOIN dim.store AS s ON f.store_id = s.store_id
    INNER JOIN dim.[Date] AS d ON f.date_id = d.date_id
    order by c.customer_id