# Day 006 — SQL Joins, Aggregation and Row Granularity

**Program date:** Friday, 13 November 2026  
**Track:** SQL  
**Next topic:** Data modelling — star schema for order analytics

## 1. Today's learning objectives

Today's SQL practice focused on how joins affect returned rows and how aggregation changes the level of detail in a result.

Topics covered:

- `INNER JOIN` versus `LEFT JOIN`.
- Customer-level spending and order summaries.
- `GROUP BY` with `COUNT()` and `SUM()`.
- Replacing `NULL` with a chosen value using `COALESCE()`.
- Comparing `COUNT(*)` with `COUNT(o.order_id)`.
- Understanding detail-level results versus aggregated results.
- Understanding why a JOIN does not require `GROUP BY`.

## 2. Queries implemented

The following are the queries shared during the practice session, with formatting adjusted for readability.

### Query 1 — INNER JOIN: total order amount per customer

```sql
SELECT
    c.customer_id,
    SUM(o.amount) AS total_amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY SUM(o.amount) DESC;
```

**What it does:** Matches customers to their orders, groups the matched rows by customer, calculates each customer's total order amount, and sorts by total amount from highest to lowest.

**Important observation:** Customers with no matching order are absent because this is an `INNER JOIN`.

### Query 2 — LEFT JOIN: total order amount for every customer

```sql
SELECT
    c.customer_id,
    COALESCE(SUM(o.amount), 0) AS total_amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY COALESCE(SUM(o.amount), 0) DESC;
```

**What it does:** Keeps every customer from the left-side `customers` table. A customer with no matching order remains in the result; `SUM(o.amount)` is `NULL` for that group, and `COALESCE()` displays `0` instead.

**Important observation:** `NULL` and zero are not the same database value. In this report, zero is chosen as the presentation value for a customer with no recorded order amount.

### Query 3 — Customer-level summary

```sql
SELECT
    c.customer_id,
    c.customer_name,
    COALESCE(COUNT(o.order_id), 0) AS total_orders,
    COALESCE(SUM(o.amount), 0) AS total_amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    COALESCE(SUM(o.amount), 0) DESC,
    COALESCE(COUNT(o.order_id), 0) DESC;
```

**What it does:** Produces one summary row per customer, including customers with no orders. It calculates order count and total spending, then sorts by spending and order count.

**Small simplification:** `COALESCE(COUNT(o.order_id), 0)` can be written as `COUNT(o.order_id)`. `COUNT()` already returns zero when there are no non-`NULL` values to count.

### Query 4 — INNER JOIN: count orders using `COUNT(o.order_id)`

```sql
SELECT
    c.customer_id,
    COUNT(o.order_id) AS total_orders
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY COUNT(o.order_id) DESC;
```

### Query 5 — INNER JOIN: count joined rows using `COUNT(*)`

```sql
SELECT
    c.customer_id,
    COUNT(*) AS total_orders
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY COUNT(*) DESC;
```

**Finding:** With this `INNER JOIN`, the two counts are equal when `orders.order_id` is non-`NULL` for every real order (as expected when it is the order table's primary key). Every joined row represents a matched order.

### Query 6 — LEFT JOIN: count orders using `COUNT(o.order_id)`

```sql
SELECT
    c.customer_id,
    COUNT(o.order_id) AS total_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY COUNT(o.order_id) DESC;
```

### Query 7 — LEFT JOIN: count joined rows using `COUNT(*)`

```sql
SELECT
    c.customer_id,
    COUNT(*) AS total_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY COUNT(*) DESC;
```

**Finding:** These two counts differ for a customer who has no order:

- `COUNT(*)` counts the preserved customer row produced by the `LEFT JOIN`, so it returns `1` for that customer.
- `COUNT(o.order_id)` ignores the `NULL` order ID, so it returns `0`.

For counting actual orders after a `LEFT JOIN`, `COUNT(o.order_id)` is the appropriate expression when `order_id` is non-`NULL` for each actual order.

## 3. Key concepts learned

### A. INNER JOIN

`INNER JOIN` returns rows for which the join condition matches in both tables.

In this exercise:

```sql
ON c.customer_id = o.customer_id
```

The database matches customer IDs across the two tables. A customer who has no matching order does not appear in the INNER JOIN result.

The customer ID is normally the primary key in `customers` and a foreign key in `orders`. The matching column in the orders table does not need to be a primary key.

### B. LEFT JOIN

`LEFT JOIN` preserves all rows from the left table (`customers` here).

- When a matching order exists, order columns contain the matching values.
- When no order exists, the customer still appears and the columns from `orders` are `NULL`.

### C. JOIN and GROUP BY do different jobs

A JOIN combines related rows from tables. `GROUP BY` groups the resulting rows, commonly so aggregate functions can calculate a value per group.

A JOIN does **not** require `GROUP BY`.

For example, this is a valid detail-level query without aggregation:

```sql
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

And this LEFT JOIN also works without `GROUP BY`:

```sql
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.amount
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

When a customer has three orders, the joined detail result normally contains three rows for that customer — one row for each matching order. A subsequent `GROUP BY` can combine those rows into one customer-level summary.

### D. COUNT(*) versus COUNT(column)

- `COUNT(*)` counts result rows, including rows whose columns contain `NULL`.
- `COUNT(expression)` counts only rows where that expression is not `NULL`.

That is why `COUNT(*)` and `COUNT(o.order_id)` can differ after a LEFT JOIN.

### E. SUM() and COALESCE()

`SUM(o.amount)` returns `NULL` for a group with no non-`NULL` amount values. `COALESCE(SUM(o.amount), 0)` chooses zero as the displayed fallback.

This is a reporting decision: zero is useful when the desired interpretation is “no recorded spending,” but it should not be confused with an actual order whose amount is zero or with unknown/missing amount data.

## 4. What was done correctly

The learner correctly demonstrated the following:

- Used the customer ID relationship to join the two tables.
- Explained why an INNER JOIN excludes customers without matching orders.
- Explained why a LEFT JOIN retains all customers from the left table.
- Used `SUM()` to calculate spending per customer.
- Used `COUNT(o.order_id)` to count actual orders.
- Used `GROUP BY` to produce a customer-level summary.
- Used `COALESCE()` to present a zero instead of a `NULL` total where that was the intended reporting choice.
- Recognized that a one-to-many customer-to-orders relationship can produce multiple joined rows for one customer.
- Explained why `COUNT(*)` can return one for a customer with no orders after a LEFT JOIN, while `COUNT(o.order_id)` returns zero.
- Understood that a JOIN can return detail rows without a `GROUP BY`.

## 5. Corrections and clarifications — assistant review

This section records where the earlier guidance needed to be clearer or more precise.

### Clarification 1 — The original aggregation queries were valid

The first two queries were valid customer-spending aggregation queries. The later review correctly pointed out that they did not return individual order-detail rows, but the distinction should have been explained as a difference in **output grain**, not as a problem with the SQL itself.

### Clarification 2 — JOIN does not require GROUP BY

The earlier instruction to write detail-level INNER JOIN and LEFT JOIN queries without `GROUP BY` was intended to show individual customer-order records. It was not a SQL syntax requirement for joins.

The assistant should have made that distinction explicit immediately. JOIN can be used with or without aggregation.

### Clarification 3 — “Order-level” was the wrong label for grouped count queries

The learner labelled the grouped count queries as “order-level.” Because the queries use `GROUP BY c.customer_id`, their output is one row per customer, with an order count. They are **customer-level order-count summaries**, not individual order-level detail results.

### Clarification 4 — COALESCE around COUNT is unnecessary here

`COALESCE(COUNT(o.order_id), 0)` is valid but redundant. `COUNT(o.order_id)` already returns zero when there are no non-`NULL` order IDs in the group.

### Clarification 5 — Do not call repeated customer IDs duplicate orders

In a one-to-many join, a customer's ID appears once for each matching order. That repetition is expected, not automatically a duplicate-data problem. Duplicate detection must be based on the intended row grain and a suitable key (for example, `order_id` for order-detail rows).

## 6. Assessment status

| Skill / deliverable | Review status |
|---|---|
| INNER JOIN behavior explained | Demonstrated |
| LEFT JOIN behavior explained | Demonstrated |
| Customer spending aggregation | Implemented |
| Customer-level order summary | Implemented |
| `COUNT(*)` vs `COUNT(order_id)` with INNER JOIN | Implemented |
| `COUNT(*)` vs `COUNT(order_id)` with LEFT JOIN | Implemented |
| JOIN without `GROUP BY` understood | Discussed and understood |
| Actual row counts and duplicate checks against the live database | Not recorded in this README |

**Evidence note:** The SQL code above is the code shared in the practice conversation. Actual execution outputs, database row counts, and screenshots were not supplied in that conversation, so this README does not invent them.

## 7. Next SQL exercise — Data Modelling: Star Schema for Order Analytics

The next exercise is separate from today's JOIN practice.

### Objective

Design a small star schema for order analytics.

### Required work

1. Define the **fact table grain**: state exactly what one row in the fact table represents.
2. Identify the fact table and its measures.
3. Identify the relevant dimension tables.
4. Define primary keys and foreign-key relationships.
5. Consider two Slowly Changing Dimension (SCD) requirements and explain how they would be handled.
6. Draw an ERD or schema sketch.

### Expected deliverables

- A clear fact-table grain statement.
- A star-schema diagram or schema sketch.
- Fact and dimension table definitions.
- Primary-key and foreign-key relationships.
- Two SCD considerations with brief explanations.

Do not start by writing SQL DDL. First design the model and justify its grain, dimensions, keys, and SCD choices. The implementation can follow after the design is reviewed.

---

## 8. Final takeaway

Today's central lesson:

**JOIN determines how records from tables are matched. GROUP BY determines how matching rows are grouped for aggregation. The output grain tells you whether the result represents individual orders or a summary per customer.**

This distinction is foundational for analytical SQL and dimensional data modelling.
