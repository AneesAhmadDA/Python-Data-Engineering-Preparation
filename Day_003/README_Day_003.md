# Day 003 — SQL CTEs, Window Functions & Python Record Validation

## Overview

Day 003 contains practical SQL and Python exercises completed as part of my Data Engineering preparation.

The exercises focus on:
- Using Common Table Expressions (CTEs) to organize multi-step SQL transformations.
- Calculating customer lifetime value (CLV).
- Ranking customers within their regions using a window function.
- Validating structured event records with Python dictionaries.
- Detecting missing fields and empty values.

## 1. SQL — Customer Lifetime Value and Regional Ranking

### Objective

Calculate each customer's total order value, then rank customers within their respective regions by lifetime value.

### Database prerequisites

The query uses the existing `customers` and `orders` tables. The `customers` table must contain a `region` column, and that column should be populated before running the ranking query.

The SQL file includes commented-out `ALTER TABLE` and `UPDATE` statements illustrating how the region column can be added and populated. Review and execute the appropriate setup statements if the column is not already available.

### Concepts practised

- `ALTER TABLE` and `UPDATE`.
- `LEFT JOIN` to retain customers with no matching orders.
- `SUM()` and `COALESCE()`.
- Common Table Expressions (CTEs).
- Multiple CTEs in one query.
- Window functions.
- `DENSE_RANK()` with `PARTITION BY` and `ORDER BY`.

### Query workflow

1. The first CTE aggregates order amounts for each customer and region to calculate customer lifetime value.
2. The second CTE applies `DENSE_RANK()` separately within each region.
3. The final `SELECT` returns each customer's lifetime value and regional rank.

`DENSE_RANK()` assigns the same rank to tied values and does not leave gaps in subsequent ranks. For example, values 5000, 5000, and 3000 receive ranks 1, 1, and 2.

**SQL environment:** Microsoft SQL Server / SQL Server Management Studio (SSMS).

## 2. Python — Dictionary Record Validation

### Objective

Create a reusable function that accepts one dictionary representing an event record and checks that required fields exist and contain usable values.

### Required fields

- `record_id`
- `event_type`
- `event_timestamp`

### Validation logic implemented

The `validate_record(record)` function:
1. Checks whether the input is a dictionary using `isinstance()`.
2. Defines the required fields.
3. Identifies missing keys using dictionary membership.
4. Checks required values for `None` and blank or whitespace-only strings.
5. Prints validation messages and returns a Boolean result.

### Test cases

Ten sample records are defined, including:
- Five records with all required fields populated.
- Records with missing or incorrectly named keys.
- Records with blank or whitespace-only values.

### Concepts practised

- Function definitions and parameters.
- Dictionaries and key-value pairs.
- `isinstance()`.
- Lists and list comprehensions.
- Dictionary key membership with `in`.
- Dictionary value access.
- `None` checks.
- String `.strip()` for whitespace validation.
- Conditional statements and Boolean return values.

## 3. Known Follow-up Fix

The submitted Python code detects `empty_fields` and prints an error message, but it does not return `False` afterward. It then prints the record as valid and returns `True`.

Consequently, records with blank values (such as Record8 and Record9) are currently misclassified as valid.

**Follow-up:** Return `False` when `empty_fields` is non-empty. Print the valid-record message and return `True` only after all validation checks have passed.

This limitation is documented so the README accurately reflects the submitted implementation rather than claiming that every test passes.

## 4. Suggested Repository Structure

```text
Internship_prep/
├── Day_002/
│   └── ...
└── Day_003/
    ├── README.md
    ├── Day_003.sql
    └── Day_003.py
```

Use the filenames that match your actual files. Keep the SQL and Python exercises in separate files.

## 5. How to Run

### SQL

1. Open the SQL script in SQL Server Management Studio.
2. Connect to the SQL Server instance containing `customers` and `orders`.
3. Confirm that `customers.region` exists and is populated.
4. Execute the CTE and ranking query.
5. Inspect the customer lifetime values and regional ranks.

### Python

From the Day_003 directory, run:

```bash
python Day_003.py
```

Replace the filename if your Python script has a different name.

## 6. Learning Outcomes

- Structuring SQL logic with CTEs.
- Aggregating data at customer level.
- Applying window functions for within-group ranking.
- Preserving unmatched customers with `LEFT JOIN`.
- Handling missing aggregate values with `COALESCE()`.
- Validating structured records before downstream processing.
- Identifying validation-control-flow bugs.

## 7. Practice Status

| Area | Status |
|---|---|
| Customer region setup | Setup statements included as comments; verify execution |
| Customer lifetime value aggregation | Implemented in CTE |
| Regional customer ranking | Implemented with `DENSE_RANK()` |
| Python dictionary type check | Implemented |
| Required-key validation | Implemented |
| Empty-value detection | Implemented |
| Rejecting empty-value records | Follow-up fix required |
| Final validation test review | Pending after the follow-up fix |

**Learning approach:** Implement independently, inspect the output, understand errors, and improve the solution incrementally.
