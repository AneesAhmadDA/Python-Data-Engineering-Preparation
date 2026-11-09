# Day 002 — Python, SQL, Iterators & Generators Practice

## Overview

This repository contains my Day 002 practice exercises as part of my preparation for a career in Data Engineering.

The work covers two areas:

1. **SQL fundamentals** — creating relational tables, inserting records, filtering data, joining tables, and performing aggregations.
2. **Python fundamentals** — implementing a custom iterator, creating a generator with `yield`, and reading and counting records from a text file.

The purpose of these exercises is to strengthen practical coding skills and understand how the concepts work, rather than simply memorising syntax.

---

## 1. SQL Practice

### Database

Database name: `internship_prep`

The exercise uses two related tables:

#### `customers`

| Column | Data type | Constraint |
|---|---|---|
| `customer_id` | `INT` | Primary key |
| `customer_name` | `VARCHAR(50)` | Not null |
| `city` | `VARCHAR(50)` | Not null |

#### `orders`

| Column | Data type | Constraint |
|---|---|---|
| `order_id` | `INT` | Primary key |
| `customer_id` | `INT` | Not null, foreign key referencing `customers.customer_id` |
| `amount` | `DECIMAL(10,2)` | Not null |

### SQL concepts practised

- Creating and selecting a database.
- Creating tables and defining columns.
- Primary key and foreign key constraints.
- `NOT NULL` constraints.
- Inserting multiple records with one `INSERT` statement.
- Filtering rows with `WHERE`.
- Comparison operators.
- Joining related tables with `INNER JOIN` and `LEFT JOIN`.
- Aggregating values with `SUM()`.
- Grouping records with `GROUP BY`.
- Sorting results with `ORDER BY`.
- Handling `NULL` aggregate results with `COALESCE()`.

### Queries implemented

1. Retrieve customers whose city is Peshawar.
2. Retrieve orders with an amount greater than 3,000.
3. Calculate the total order amount for each customer, including customers with no orders.
4. Join customers and orders to display customer and order details.
5. Calculate total order revenue by city.

### SQL environment

The script uses Microsoft SQL Server syntax, including `USE` and `OBJECT_ID()`. It can be run in SQL Server Management Studio (SSMS) or another SQL Server-compatible client.

---

## 2. Python Iterator Practice

A custom iterator class named `counter` was implemented.

The class maintains its current position and defines:

- `__iter__()` to return the iterator object.
- `__next__()` to return the next value.
- `StopIteration` to signal that no more values are available.

The iterator was tested by iterating over a counter configured to produce five values.

### Concepts practised

- Iterable and iterator concepts.
- The iterator protocol.
- `iter()` and `next()` concepts.
- Object state.
- `__iter__()` and `__next__()`.
- `StopIteration`.

---

## 3. Python Generator Practice

A generator function named `gen()` was implemented using `yield`.

It produces integers from a supplied starting value to a supplied ending value, inclusive.

The generator was created for the range 10 to 20, and successive values were retrieved using `next()`.

### Concepts practised

- Generator functions.
- The `yield` keyword.
- Generator objects.
- Lazy evaluation.
- Sequential value production.
- Consuming generators with `next()`.

---

## 4. Text File Processing Practice

A sample event file named `event.txt` was created with five records containing `Login` and `Logout` events.

The file was opened using a context manager:

```python
with open("event.txt", "r") as file:
    ...
```

The file was processed sequentially, and the program counted:

- Total number of records.
- Number of `Login` records.
- Number of `Logout` records.

### Concepts practised

- Creating and writing a text file.
- Reading a file line by line.
- Using `with open(...)` for file handling.
- Removing surrounding whitespace with `strip()`.
- Searching for text within a line.
- Maintaining counters while processing records.

### Sample expected counts

For the five sample records:

| Metric | Expected count |
|---|---:|
| Total records | 5 |
| Login records | 3 |
| Logout records | 2 |

---

## 5. Current Scope and Follow-up Work

The following exercises were implemented:

- Custom iterator.
- Generator function using `yield`.
- Sequential generator consumption using `next()`.
- Text file creation.
- Normal line-by-line file reading and event counting.

The following parts are **follow-up work**, not yet demonstrated in the submitted implementation:

- Reading the event file through a dedicated generator function.
- Comparing normal file processing with generator-based file processing.
- Measuring and documenting memory usage for both approaches.
- Demonstrating generator exhaustion and explaining `StopIteration` after all values are consumed.

These are useful next steps for developing a stronger understanding of memory-aware data processing.

---

## 6. Suggested Repository Structure

```text
Day_002/
├── README.md
├── Day_002.py
├── SQL_Day_002.sql
└── event.txt
```

Use the filenames that match your actual files. If your SQL script or event file is stored elsewhere, adjust the structure accordingly.

---

## 7. Key Learning Outcomes

By completing this practice, I worked with:

- Relational database design and table relationships.
- SQL filtering, joins, grouping, and aggregation.
- Primary keys, foreign keys, and data constraints.
- Python classes and the iterator protocol.
- Generator functions and lazy evaluation.
- Sequential file processing.
- Basic event-record counting.

These concepts provide a foundation for later work involving Python ETL scripts, data ingestion, and processing larger datasets.

---

## 8. How to Run

### Python

From the directory containing the Python script:

```bash
python Day_002.py
```

The script creates `event.txt` in the current working directory when it runs.

### SQL Server

1. Open the SQL script in SQL Server Management Studio.
2. Connect to your SQL Server instance.
3. Execute the script against the intended development instance.
4. Inspect the query results.

**Note:** The SQL setup script is intended for practice. Review its database/table creation and drop order before rerunning it, especially because the `orders` table references `customers`.

---

## 9. Practice Status

| Area | Status |
|---|---|
| SQL database and table creation | Practised |
| SQL inserts and constraints | Practised |
| SQL filtering | Practised |
| SQL joins | Practised |
| SQL aggregation and grouping | Practised |
| Custom Python iterator | Implemented |
| Python generator function | Implemented |
| Normal text-file processing | Implemented |
| Generator-based file processing | Follow-up |
| Memory comparison | Follow-up |
| Generator exhaustion demonstration | Follow-up |

---

**Learning approach:** Build independently, test the result, understand errors, and improve the implementation incrementally.
