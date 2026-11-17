# Day 008 — Python OOP: CSV ETL Pipeline

## Project overview

This exercise builds a small ETL workflow in Python using **Pandas** and a class-based structure. The pipeline reads a raw grocery-sales CSV file, inspects and cleans the data, and writes the transformed records to a new CSV file.

## Objectives

- Practise organizing an ETL workflow with a Python class.
- Read a CSV file into a Pandas DataFrame.
- Inspect the data before and after transformation.
- Identify and remove duplicate transaction IDs.
- Handle missing numeric values.
- Export the cleaned data without writing the DataFrame index as an extra CSV column.

## Input and output

| Item | Description |
|---|---|
| Input file | `grocery_sales_raw.csv` |
| Output file | `Cleaned_data.csv` |
| Library | `pandas` |
| Main class | `pipline` |

The script currently uses an absolute Windows path for the input file. The output path is relative, so `Cleaned_data.csv` is written to the process's current working directory unless an absolute output path is supplied.

## ETL workflow

### 1. Extraction — `extraction(path)`

- Accepts the input CSV path.
- Reads the file with `pd.read_csv()`.
- Displays the first five records.
- Returns the DataFrame for the next stage.

### 2. Transformation — `transformation(df)`

- Copies the input DataFrame so the original object is not modified by the cleaning steps.
- Displays descriptive statistics and missing-value counts.
- Finds every row associated with a duplicated `transaction_id` using `duplicated(keep=False)`.
- Removes duplicate transaction IDs while keeping the first occurrence.
- Checks that no duplicate transaction IDs remain.
- Replaces missing numeric values with the mean of the relevant column.
- Reports remaining null values and displays the final DataFrame information and descriptive statistics.

### 3. Loading — `load(df, output_path)`

- Writes the transformed DataFrame to the requested CSV path.
- Uses `index=False` so Pandas does not add its DataFrame index as an extra column.
- Prints a completion message.

## How to run

1. Make sure Python and Pandas are installed:

   ```powershell
   python -m pip install pandas
   ```

2. Update the input path in the script so it points to the location of `grocery_sales_raw.csv` on your computer.

3. Run the Python file from PowerShell or the VS Code terminal:

   ```powershell
   python your_script_name.py
   ```

4. Check the terminal output and confirm that `Cleaned_data.csv` was created in the current working directory (or at the output path you supplied).

## Current OOP design

The current implementation uses one class, `pipline`, with three methods:

- `extraction()` — performs the reader responsibility.
- `transformation()` — performs cleaning and contains the duplicate/null checks.
- `load()` — writes the transformed data.

The script's final statements instantiate the class and call the methods in ETL order. This demonstrates class instantiation, method calls, passing data between methods, and a basic class-based workflow.

**Design limitation:** the reader, validator, and pipeline orchestration are not yet independent reusable components. Validation is embedded inside `transformation()`, and the orchestration is performed by the top-level script rather than a separate coordinator class. Therefore, this is a useful first class-based ETL implementation, but it does not fully demonstrate the separate reader / validator / pipeline-coordinator design objective.

## Data-quality decisions and trade-offs

### Duplicate handling

The pipeline treats `transaction_id` as the key used to identify duplicates and keeps the first row for each repeated ID. This is simple and deterministic, but it is a business-rule decision: when two rows with the same ID contain different values, the later row is discarded. A production pipeline should define how conflicting duplicate records are resolved rather than assuming that the first record is always correct.

### Missing numeric values

The pipeline fills missing numeric values using each column's mean. This is straightforward for practice data, but the mean can be affected by outliers and may not be suitable for every numeric field. Numeric identifiers such as `transaction_id` should not be imputed; the current loop does not explicitly exclude identifier columns. Non-numeric columns with missing values are reported as skipped, not filled.

## Known limitations / next improvements

- Rename `pipline` to `Pipeline` (the current spelling works, but `Pipeline` is clearer and follows the usual Python class-naming convention).
- Exclude identifier columns such as `transaction_id` from numeric mean imputation.
- Separate the reader, validator, and pipeline coordinator into distinct classes if completing the full OOP component-design objective.
- Add error handling for a missing input file, invalid data, or a failed output write.
- Consider returning the output path or a load status from `load()`.
- Add a validation step after saving to confirm that the output file exists and can be read.

## Completion assessment

| Exercise element | Current status |
|---|---|
| CSV extraction | Implemented |
| Data inspection | Implemented |
| Duplicate detection and removal | Implemented |
| Missing numeric-value handling | Implemented, with the identifier-column limitation noted above |
| CSV loading with `index=False` | Implemented |
| Basic class and method usage | Implemented |
| Separate reader / validator / coordinator components | Partially implemented; responsibilities are currently combined |
| Record a trade-off | Documented above |
| README documentation | Completed |

**Overall:** the basic ETL workflow is implemented. The full OOP design objective is not yet complete until the responsibilities are separated into reusable components.
