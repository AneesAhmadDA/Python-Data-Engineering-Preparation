--THis is the use of inner join to get the total amount of orders for each customer. The query selects the customer_id and the sum of the order amounts, groups the results by customer_id, and orders them in descending order based on the total amount.
select c.customer_id, SUM(o.amount) as total_amount
        from customers c
        INNER JOIN orders o
        ON c.customer_id = o.customer_id
        group by c.customer_id
        order by SUM(o.amount) DESC; 
--Now checkin the order amount for all customers includeing those who havent placed an order 
select c.customer_id, COALESCE(SUM(o.amount),0) as total_amount
        from customers c
        LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        group by c.customer_id
        order by COALESCE(SUM(o.amount),0) DESC; 

--Generating the customer_level Summary 
select c.customer_id,c.customer_name,COALESCE(COUNT(o.order_id),0) AS total_orders, COALESCE(SUM(o.amount),0) as total_amount
        from customers c
        LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        group by c.customer_id,c.customer_name
        order by COALESCE(SUM(o.amount),0) DESC, COALESCE(COUNT(o.order_id),0) DESC; 

--order level inner join using count(order_id)
select c.customer_id, COUNT(o.order_id) as total_orders
        from customers c
        INNER JOIN orders o
        ON c.customer_id = o.customer_id
        group by c.customer_id
        order by COUNT(o.order_id) DESC; 

--order level inner join using count(*)
select c.customer_id, COUNT(*) as total_orders
        from customers c
        INNER JOIN orders o
        ON c.customer_id = o.customer_id
        group by c.customer_id
        order by COUNT(*) DESC; 
-----------------LEFT JOIN----------------------------
--order level Left join using count(order_id)
select c.customer_id, COUNT(o.order_id) as total_orders
        from customers c
        LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        group by c.customer_id
        order by COUNT(o.order_id) DESC; 

--order level Left join using count(*)
select c.customer_id, COUNT(*) as total_orders
        from customers c
        LEFT JOIN orders o
        ON c.customer_id = o.customer_id
        group by c.customer_id
        order by COUNT(*) DESC; 

--NOW EXECUTING WITHOUT USING THE GROUP BY CLAUSE
--THIS IS INNER JOIN
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.amount
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id;

--THIS IS LEFT JOIN
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.amount
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id;