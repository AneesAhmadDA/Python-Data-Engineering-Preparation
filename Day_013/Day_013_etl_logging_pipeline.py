from pathlib import Path
import logging

import pandas as pd


# This script is expected to be saved in:
# Internship_prep/Day_013/Python/etl_logging_pipeline.py
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]

# Reuse the raw dataset from Day 008. Keep that original dataset unchanged.
INPUT_FILE = PROJECT_ROOT / "Day_008" / "grocery_sales_raw.csv"
OUTPUT_FILE = SCRIPT_DIR / "Cleaned_data.csv"
LOG_FILE = SCRIPT_DIR / "logs" / "etl_pipeline.log"


def configure_logger(log_file: Path) -> logging.Logger:
    """Create one logger that writes to both the terminal and a log file."""
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("grocery_etl")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Prevent duplicate messages if this configuration is called more than once.
    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler 1: send log messages to the terminal.
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Handler 2: save the same log messages to a file.
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


class Pipeline:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def extraction(self, path: Path) -> pd.DataFrame:
        self.logger.info("EXTRACTION: started")
        self.logger.info("Reading source file: %s", path)

        df = pd.read_csv(path)

        self.logger.info(
            "EXTRACTION: completed | rows=%d | columns=%d",
            len(df),
            len(df.columns),
        )
        self.logger.info("First five rows:\n%s", df.head().to_string(index=False))
        return df

    def transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("TRANSFORMATION: started")
        df = df.copy()  # Keep the original DataFrame unchanged.

        if "transaction_id" not in df.columns:
            raise KeyError("Required column 'transaction_id' was not found.")

        self.logger.info("Rows received for transformation: %d", len(df))
        self.logger.info(
            "Numeric summary before transformation:\n%s",
            df.describe().to_string(),
        )

        # 1. Find duplicate transaction IDs.
        duplicate_mask = df.duplicated(subset=["transaction_id"], keep=False)
        duplicate_rows = int(duplicate_mask.sum())

        if duplicate_rows:
            self.logger.warning(
                "Found %d rows involved in duplicate transaction_id values.",
                duplicate_rows,
            )
            self.logger.warning(
                "Duplicate records:\n%s",
                df.loc[duplicate_mask].to_string(index=False),
            )
        else:
            self.logger.info("No duplicate transaction IDs were found.")

        # Keep the first row for each transaction ID, matching your earlier rule.
        rows_before_deduplication = len(df)
        df = df.drop_duplicates(subset=["transaction_id"], keep="first")
        removed_rows = rows_before_deduplication - len(df)

        self.logger.info(
            "Deduplication completed | removed=%d | remaining=%d",
            removed_rows,
            len(df),
        )

        # 2. Inspect missing values and handle missing numeric values.
        missing_counts = df.isna().sum()
        columns_with_missing_values = missing_counts[missing_counts > 0]

        if columns_with_missing_values.empty:
            self.logger.info("No missing values were found after deduplication.")
        else:
            for column, missing_count in columns_with_missing_values.items():
                self.logger.warning(
                    "Column '%s' contains %d missing value(s).",
                    column,
                    int(missing_count),
                )

                # Never calculate an average for an identifier column.
                if column == "transaction_id":
                    self.logger.warning(
                        "Missing transaction IDs will not be imputed; they need a data-quality rule."
                    )
                    continue

                if pd.api.types.is_numeric_dtype(df[column]):
                    mean_value = df[column].mean()

                    if pd.isna(mean_value):
                        self.logger.warning(
                            "Cannot calculate a mean for '%s'; its missing values remain.",
                            column,
                        )
                        continue

                    df[column] = df[column].fillna(mean_value)
                    self.logger.info(
                        "Imputed missing values in '%s' using mean=%s.",
                        column,
                        mean_value,
                    )
                else:
                    self.logger.warning(
                        "'%s' is non-numeric; missing values were not imputed.",
                        column,
                    )

        # 3. Verify the result instead of assuming every missing value was fixed.
        remaining_missing = df.isna().sum()
        remaining_total = int(remaining_missing.sum())

        if remaining_total == 0:
            self.logger.info("Validation passed: no missing values remain.")
        else:
            self.logger.warning(
                "Validation found %d missing value(s) still remaining:\n%s",
                remaining_total,
                remaining_missing[remaining_missing > 0].to_string(),
            )

        self.logger.info(
            "Numeric summary after transformation:\n%s",
            df.describe().to_string(),
        )
        self.logger.info("Final data types:\n%s", df.dtypes.to_string())
        self.logger.info(
            "TRANSFORMATION: completed | rows=%d | columns=%d",
            len(df),
            len(df.columns),
        )
        return df

    def load(self, df: pd.DataFrame, output_path: Path) -> None:
        self.logger.info("LOAD: started")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)

        self.logger.info(
            "LOAD: completed | rows_saved=%d | output_file=%s",
            len(df),
            output_path,
        )

    def run(self, input_path: Path, output_path: Path) -> None:
        self.logger.info("=" * 65)
        self.logger.info("ETL PIPELINE: started")

        try:
            df = self.extraction(input_path)
            df = self.transformation(df)
            self.load(df, output_path)
        except Exception:
            # logger.exception records the error message and the traceback.
            self.logger.exception("ETL PIPELINE: failed")
            raise

        self.logger.info("ETL PIPELINE: completed successfully")
        self.logger.info("=" * 65)


if __name__ == "__main__":
    logger = configure_logger(LOG_FILE)
    pipeline = Pipeline(logger)

    try:
        pipeline.run(INPUT_FILE, OUTPUT_FILE)
    except Exception:
        logger.error("Execution stopped. Review the ERROR entry in the log file.")
        raise SystemExit(1)
