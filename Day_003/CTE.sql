--since customer table already exist i will just add the region coulmn to the table
--ALTER TABLE customers
--ADD region VARCHAR(50) NOT NULL DEFAULT 'Unknown';
---update customers
---set region ='North'
--where city = 'Peshawar';
--update customers
--set region ='South'
--where city in ('Lahore','islamabad');

---select * from orders
select * from customers;
select * from orders;

--now lets solve the problem using two CTE calculate customer lifetime value and rank customers by value within each region.
with CTE as(
    select c.customer_id,c.region,SUM(COALESCE(o.amount,0)) as life_time_value from customers c
        Left JOIN orders o on c.customer_id=o.customer_id
        group by c.customer_id,c.region
),
Rank_CTE as (
    select customer_id,region,life_time_value,
        DENSE_RANK()OVER(PARTITION BY region ORDER BY life_time_value desc) as regional_rank
    FROM CTE 
)
select * from Rank_CTE;
