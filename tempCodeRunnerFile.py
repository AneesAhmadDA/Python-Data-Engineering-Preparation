"""ETL project: Top 10 largest banks by market capitalization.

Extracts the "By market capitalization" table from the supplied archived
Wikipedia page, converts USD market caps to GBP/EUR/INR using the supplied
exchange-rate CSV, and saves the result to CSV and SQLite.

Run:
    pip install requests beautifulsoup4 pandas lxml
    python banks_project.py

The output files are created in the current working directory:
    Largest_banks_data.csv
    Banks.db
    code_log.txt
"""

from __future__ import annotations

import logging
import re
import sqlite3
import sys
from io import StringIO
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests
from bs4 import BeautifulSoup


# -----------------------------------------------------------------------------
# Project configuration
# -----------------------------------------------------------------------------
DATA_URL = (
    "https://web.archive.org/web/20230908091635/"
    "https://en.wikipedia.org/wiki/List_of_largest_banks"
)
EXCHANGE_RATE_CSV = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv"
)
OUTPUT_CSV = Path("./Largest_banks_data.csv")
DATABASE_FILE = Path("./Banks.db")
TABLE_NAME = "Largest_banks"
LOG_FILE = Path("./code_log.txt")

EXTRACTED_COLUMNS = ["Name", "MC_USD_Billion"]
FINAL_COLUMNS = [
    "Name",
    "MC_USD_Billion",
    "MC_GBP_Billion",
    "MC_EUR_Billion",
    "MC_INR_Billion",
]

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; BanksETLProject/1.0)"
}
REQUEST_TIMEOUT_SECONDS = 30


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
def log_progress(message: str) -> None:
    """Write a timestamped progress message to code_log.txt and the console."""
    logging.info(message)


def configure_logging() -> None:
    """Configure append-only timestamped logging."""
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="a",
        force=True,
    )
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
    logging.getLogger().addHandler(console)


# -----------------------------------------------------------------------------
# Extraction helpers
# -----------------------------------------------------------------------------
def _flatten_column_name(column: object) -> str:
    """Convert normal or multi-level pandas column labels into plain text."""
    if isinstance(column, tuple):
        parts = [str(part).strip() for part in column if str(part).strip() and "Unnamed" not in str(part)]
        return " ".join(parts)
    return str(column).strip()


def _normalise_header(value: object) -> str:
    text = _flatten_column_name(value).lower()
    text = text.replace("&", "and")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _find_relevant_columns(frame: pd.DataFrame) -> tuple[object, object] | None:
    """Identify the bank-name and USD-market-cap columns in a parsed table."""
    name_column = None
    market_cap_column = None

    for column in frame.columns:
        header = _normalise_header(column)
        if market_cap_column is None and (
            "market cap" in header or "market capitalization" in header
        ):
            market_cap_column = column
        if name_column is None and (
            header == "name"
            or "bank name" in header
            or header == "bank"
            or header.endswith(" bank name")
        ):
            name_column = column

    # Some archived versions have abbreviated or slightly different headers.
    if market_cap_column is None:
        for column in frame.columns:
            header = _normalise_header(column)
            if "usd" in header and ("billion" in header or "market" in header):
                market_cap_column = column
                break

    if name_column is None:
        for column in frame.columns:
            header = _normalise_header(column)
            if "rank" not in header and column != market_cap_column:
                name_column = column
                break

    if name_column is None or market_cap_column is None:
        return None
    return name_column, market_cap_column


def _find_target_table(soup: BeautifulSoup) -> pd.DataFrame:
    """Find the table associated with the 'By market capitalization' heading.

    It first searches tables appearing after the matching heading. If the
    archived HTML has altered heading markup, it scans all page tables and
    selects the one whose headers identify bank names and market capitalization.
    """
    heading = None
    for candidate in soup.find_all(["h1", "h2", "h3", "h4"]):
        heading_text = " ".join(candidate.get_text(" ", strip=True).split()).lower()
        if "by market capitalization" in heading_text:
            heading = candidate
            break

    tables_to_check: list[object] = []
    if heading is not None:
        tables_to_check.extend(heading.find_all_next("table"))
    # Include remaining tables as a fallback; avoid checking the same table twice.
    seen_ids = {id(table) for table in tables_to_check}
    for table in soup.find_all("table"):
        if id(table) not in seen_ids:
            tables_to_check.append(table)

    for table in tables_to_check:
        try:
            parsed_tables = pd.read_html(StringIO(str(table)))
        except (ValueError, ImportError):
            continue
        if not parsed_tables:
            continue
        frame = parsed_tables[0]
        if _find_relevant_columns(frame) is not None:
            return frame

    raise ValueError(
        "Could not find a table containing bank names and market-capitalization "
        "values. Check whether the archived page structure has changed."
    )


def _parse_market_cap(value: object) -> float | None:
    """Convert a market-cap cell such as '$469.81' or '469.81' to float."""
    if pd.isna(value):
        return None
    text = str(value).strip().replace(",", "")
    # Remove footnote markers such as [1] and currency/unit labels.
    text = re.sub(r"\[[^\]]*\]", "", text)
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def _clean_bank_name(value: object) -> str:
    """Return a clean bank name from a table cell."""
    if pd.isna(value):
        return ""
    # pandas.read_html may return a string or a cell with embedded whitespace.
    name = " ".join(str(value).replace("\xa0", " ").split())
    name = re.sub(r"\[[^\]]*\]", "", name).strip()
    return name


def extract(url: str = DATA_URL) -> pd.DataFrame:
    """Extract the top 10 banks and their market cap in USD billions."""
    log_progress("Starting data extraction from the archived Wikipedia page.")
    # Correct accidental whitespace in copied URLs (the project brief includes
    # a space before /https in the displayed URL).
    url = re.sub(r"\s+(/https?://)", r"\1", url.strip())

    response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    source_table = _find_target_table(soup)

    columns = _find_relevant_columns(source_table)
    if columns is None:
        raise ValueError("The market capitalization table has unexpected columns.")
    name_column, market_cap_column = columns

    extracted_rows: list[dict[str, object]] = []
    for _, row in source_table.iterrows():
        bank_name = _clean_bank_name(row.get(name_column))
        market_cap = _parse_market_cap(row.get(market_cap_column))
        if bank_name and market_cap is not None:
            extracted_rows.append(
                {"Name": bank_name, "MC_USD_Billion": market_cap}
            )

    if not extracted_rows:
        raise ValueError("No bank records were extracted from the market-cap table.")

    result = pd.DataFrame(extracted_rows, columns=EXTRACTED_COLUMNS)
    result = result.sort_values(
        by="MC_USD_Billion", ascending=False, kind="stable"
    ).head(10).reset_index(drop=True)
    result["MC_USD_Billion"] = result["MC_USD_Billion"].astype(float).round(2)

    if len(result) < 10:
        raise ValueError(
            f"Expected 10 banks, but only {len(result)} valid records were found."
        )

    log_progress(f"Data extraction complete: extracted {len(result)} banks.")
    return result


# -----------------------------------------------------------------------------
# Transformation
# -----------------------------------------------------------------------------
def _load_exchange_rates(csv_source: str = EXCHANGE_RATE_CSV) -> dict[str, float]:
    """Read exchange rates from the provided CSV into a currency-rate mapping."""
    rates_frame = pd.read_csv(csv_source)
    rates_frame.columns = [str(column).strip() for column in rates_frame.columns]

    if not {"Currency", "Rate"}.issubset(rates_frame.columns):
        raise ValueError(
            "Exchange-rate CSV must contain columns named 'Currency' and 'Rate'. "
            f"Found: {list(rates_frame.columns)}"
        )

    rates_frame["Currency"] = rates_frame["Currency"].astype(str).str.strip().str.upper()
    rates_frame["Rate"] = pd.to_numeric(rates_frame["Rate"], errors="coerce")
    rates_frame = rates_frame.dropna(subset=["Currency", "Rate"])
    rates = dict(zip(rates_frame["Currency"], rates_frame["Rate"].astype(float)))

    required = {"GBP", "EUR", "INR"}
    missing = required.difference(rates)
    if missing:
        raise ValueError(f"Exchange-rate CSV is missing currency codes: {sorted(missing)}")
    return rates


def transform(
    bank_dataframe: pd.DataFrame,
    exchange_rate_csv: str = EXCHANGE_RATE_CSV,
) -> pd.DataFrame:
    """Add GBP, EUR, and INR market-cap columns, rounded to two decimals.

    The supplied exchange-rate file expresses how many units of each currency
    equal one US dollar, so each USD market-cap value is multiplied by its rate.
    """
    log_progress("Starting data transformation using the exchange-rate CSV.")

    missing_columns = set(EXTRACTED_COLUMNS).difference(bank_dataframe.columns)
    if missing_columns:
        raise ValueError(f"Input dataframe is missing columns: {sorted(missing_columns)}")

    rates = _load_exchange_rates(exchange_rate_csv)
    transformed = bank_dataframe[EXTRACTED_COLUMNS].copy()
    transformed["MC_USD_Billion"] = pd.to_numeric(
        transformed["MC_USD_Billion"], errors="raise"
    ).round(2)

    for currency in ("GBP", "EUR", "INR"):
        output_column = f"MC_{currency}_Billion"
        transformed[output_column] = (
            transformed["MC_USD_Billion"] * rates[currency]
        ).round(2)

    transformed = transformed[FINAL_COLUMNS]
    log_progress("Data transformation complete: GBP, EUR, and INR columns added.")
    return transformed


# -----------------------------------------------------------------------------
# Loading
# -----------------------------------------------------------------------------
def load_to_csv(
    dataframe: pd.DataFrame,
    output_csv_path: str | Path = OUTPUT_CSV,
) -> None:
    """Save the transformed dataframe to a CSV file."""
    dataframe.to_csv(output_csv_path, index=False, encoding="utf-8")
    log_progress(f"Transformed data saved to CSV file: {output_csv_path}")


def load_to_db(
    dataframe: pd.DataFrame,
    database_name: str | Path = DATABASE_FILE,
    table_name: str = TABLE_NAME,
) -> None:
    """Load the transformed dataframe into an SQLite database table."""
    with sqlite3.connect(database_name) as connection:
        dataframe.to_sql(table_name, connection, if_exists="replace", index=False)
    log_progress(
        f"Transformed data loaded into SQLite database '{database_name}', "
        f"table '{table_name}'."
    )


# -----------------------------------------------------------------------------
# Database queries and verification
# -----------------------------------------------------------------------------
def run_queries(
    database_name: str | Path = DATABASE_FILE,
    table_name: str = TABLE_NAME,
) -> dict[str, pd.DataFrame]:
    """Run demonstration queries and return their results.

    Queries:
      1. Display every row in the final table.
      2. Calculate the average market capitalization in GBP.
      3. Display the names of the five largest banks by EUR market cap.
    """
    log_progress("Running verification queries against the SQLite database.")
    safe_table = '"' + table_name.replace('"', '""') + '"'

    queries = {
        "all_banks": f"SELECT * FROM {safe_table};",
        "average_market_cap_gbp": (
            f"SELECT ROUND(AVG(MC_GBP_Billion), 2) AS Average_MC_GBP_Billion "
            f"FROM {safe_table};"
        ),
        "top_5_banks_by_eur": (
            f"SELECT Name, MC_EUR_Billion FROM {safe_table} "
            "ORDER BY MC_EUR_Billion DESC LIMIT 5;"
        ),
    }

    results: dict[str, pd.DataFrame] = {}
    with sqlite3.connect(database_name) as connection:
        for label, query in queries.items():
            results[label] = pd.read_sql_query(query, connection)

    print("\n--- Database query: all banks ---")
    print(results["all_banks"].to_string(index=False))
    print("\n--- Database query: average market cap in GBP ---")
    print(results["average_market_cap_gbp"].to_string(index=False))
    print("\n--- Database query: top 5 banks by market cap in EUR ---")
    print(results["top_5_banks_by_eur"].to_string(index=False))

    log_progress("Database queries completed successfully.")
    return results


def verify_outputs(
    dataframe: pd.DataFrame,
    csv_path: str | Path = OUTPUT_CSV,
    database_name: str | Path = DATABASE_FILE,
    table_name: str = TABLE_NAME,
) -> None:
    """Check the output CSV and database table contain the expected columns."""
    csv_check = pd.read_csv(csv_path)
    if list(csv_check.columns) != FINAL_COLUMNS:
        raise AssertionError("CSV output does not contain the expected final columns.")
    if len(csv_check) != len(dataframe):
        raise AssertionError("CSV output row count does not match transformed data.")

    with sqlite3.connect(database_name) as connection:
        db_check = pd.read_sql_query(f'SELECT * FROM "{table_name}"', connection)
    if list(db_check.columns) != FINAL_COLUMNS:
        raise AssertionError("Database table does not contain the expected final columns.")
    if len(db_check) != len(dataframe):
        raise AssertionError("Database table row count does not match transformed data.")

    log_progress("Output verification complete: CSV and database table are valid.")


def verify_log_file() -> None:
    """Confirm key ETL milestones were recorded in code_log.txt."""
    log_progress("Checking that all required ETL stages were logged.")
    log_contents = LOG_FILE.read_text(encoding="utf-8") if LOG_FILE.exists() else ""
    required_phrases = [
        "Starting data extraction",
        "Data extraction complete",
        "Starting data transformation",
        "Data transformation complete",
        "saved to CSV file",
        "loaded into SQLite database",
        "Database queries completed successfully",
        "Output verification complete",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in log_contents]
    if missing:
        raise AssertionError(f"The log file is missing these entries: {missing}")
    log_progress("Log verification complete: all required ETL stages are recorded.")


# -----------------------------------------------------------------------------
# Main ETL workflow
# -----------------------------------------------------------------------------
def main() -> None:
    configure_logging()
    log_progress("ETL project started.")

    try:
        extracted_data = extract(DATA_URL)
        print("\n--- Extracted data (top 10 banks) ---")
        print(extracted_data.to_string(index=False))

        transformed_data = transform(extracted_data, EXCHANGE_RATE_CSV)
        print("\n--- Transformed data ---")
        print(transformed_data.to_string(index=False))

        load_to_csv(transformed_data, OUTPUT_CSV)
        load_to_db(transformed_data, DATABASE_FILE, TABLE_NAME)
        verify_outputs(transformed_data, OUTPUT_CSV, DATABASE_FILE, TABLE_NAME)
        run_queries(DATABASE_FILE, TABLE_NAME)
        verify_log_file()

        log_progress("ETL project completed successfully.")
        print("\nETL pipeline completed successfully.")
        print(f"CSV output: {OUTPUT_CSV.resolve()}")
        print(f"SQLite database: {DATABASE_FILE.resolve()}")
        print(f"Log file: {LOG_FILE.resolve()}")

    except Exception as error:
        log_progress(f"ETL project failed: {type(error).__name__}: {error}")
        raise


if __name__ == "__main__":
    main()
