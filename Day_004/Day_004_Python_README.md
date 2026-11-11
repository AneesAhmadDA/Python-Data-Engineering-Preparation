# Day 004 --- Python Practice

**Date:** 11 November 2026\
**Topics:** List comprehensions, dictionary comprehensions, and
traditional loops

## Learning Objectives

-   Filter records using list comprehensions.
-   Build a dictionary from records using a dictionary comprehension.
-   Count records that satisfy a condition.
-   Reimplement filtering logic using traditional `for` loops.
-   Compare comprehensions and loops in terms of readability and
    maintainability.

## Practice Scenario

The exercise uses synthetic ambulance telemetry records. Each record
contains an ambulance ID, speed, and status.

Example data used in the exercise:

  Ambulance ID     Speed Status
  -------------- ------- --------
  AMB001              65 ACTIVE
  AMB002               0 IDLE
  AMB003              80 ACTIVE
  AMB004              45 ACTIVE
  AMB005               0 IDLE

## Tasks

### Task 1 --- Extract active ambulances

Use a list comprehension to extract the IDs of ambulances whose status
is `ACTIVE`.

Expected result for the example data:

``` python
['AMB001', 'AMB003', 'AMB004']
```

### Task 2 --- Filter ambulances by speed

Use a list comprehension to extract ambulance IDs where speed is greater
than `50`.

Expected result:

``` python
['AMB001', 'AMB003']
```

### Task 3 --- Build an ambulance-to-speed mapping

Use a dictionary comprehension to create a mapping in which each
ambulance ID is the key and its speed is the value.

Expected result:

``` python
{
    'AMB001': 65,
    'AMB002': 0,
    'AMB003': 80,
    'AMB004': 45,
    'AMB005': 0
}
```

### Task 4 --- Count active ambulances

Calculate the number of records with status `ACTIVE`.

Expected result:

``` text
3
```

### Task 5 --- Reimplement filtering with traditional loops

Reimplement the active-ambulance filtering and speed filtering using
ordinary `for` loops rather than comprehensions.

The purpose is to understand that both approaches can produce the same
result, while expressing the logic differently.

### Task 6 --- Compare the approaches

Write a short comparison in your own words. Address:

1.  Which approach is more readable for simple filtering?
2.  Which approach is easier to maintain?
3.  When would you choose a traditional loop?
4.  When would you choose a list or dictionary comprehension?

**Status:** This written comparison remains to be recorded in the
practice notes. Do not mark the Python exercise fully complete until you
have written it.

## Key Concepts

  -----------------------------------------------------------------------
  Concept                             Meaning
  ----------------------------------- -----------------------------------
  List comprehension                  Creates a list by expressing an
                                      iteration and optional condition in
                                      a compact form.

  Dictionary comprehension            Creates a dictionary by expressing
                                      key-value generation and optional
                                      filtering.

  Conditional filtering               Includes only records that satisfy
                                      a condition.

  Traditional `for` loop              Iterates through items with
                                      explicit statements and usually
                                      builds the result incrementally.
  -----------------------------------------------------------------------

## Completion Checklist

-   [x] Extract active ambulance IDs using a list comprehension.
-   [x] Extract ambulance IDs with speed greater than 50.
-   [x] Build an ambulance ID-to-speed dictionary.
-   [x] Count active ambulances.
-   [x] Reimplement the filtering operations using traditional loops.
-   [ ] Write a comparison of comprehensions and traditional loops.

## Suggested Repository Organization

Keep this day's Python work in your existing Python practice repository.
For example:

``` text
Internship_prep/
└── Python/
    └── Day_004/
        ├── README.md
        └── day_004_comprehensions.py
```

Adapt the folder names to match your existing repository structure; do
not create another Git repository inside the existing one.

## Notes

-   The values above document the exercise example and expected results.
-   Keep your actual implementation in the Python script and ensure it
    produces the expected results.
-   This README documents the assignment and its learning objectives; it
    is not a substitute for the submitted code.
