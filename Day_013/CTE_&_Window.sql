use Internship_prep;
with ProductSales as (
    select 
        d.product_id,d.product_name,d.category,SUM(fs.total_amount) as Total_sales 
        from dim.products as d
        LEFT JOIN  fact.sales as fs
        on d.product_id=fs.product_id
        GROUP BY d.product_id,d.product_name,d.category
)
,Rank_CTE as(
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY Total_Sales DESC) AS row_num,
           RANK() OVER (PARTITION BY category ORDER BY Total_sales Desc) as Rank,
           DENSE_RANK() OVER(PARTITION BY category ORDER BY Total_sales Desc) as Dense_Rank
    FROM ProductSales
)
SELECT *
FROM Rank_CTE;

