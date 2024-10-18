# Standard imports
import sys

# Related third party imports
import pandas as pd

# Local application/library specific imports
from profiler.config import OUTPUT_PATH, SCHEMAS_PATH, setup_logging
from profiler.engine import run_engine, load_rules
from profiler.utils import remove_dir, glob_files


def main():
    logger = setup_logging()
    logger.info("Starting data quality engine")
    rules = load_rules()
    schemas = glob_files(SCHEMAS_PATH, "yaml")
    try:
        data_quality_report = run_engine(rules, schemas)
    except FileNotFoundError as e:
        logger.error(f"Attempted to read a file that does not exist: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    else:
        logger.info("Data quality engine completed successfully")

    logger.info("Writing data quality report to disk")

    remove_dir(OUTPUT_PATH)

    data_quality_report = pd.DataFrame(data_quality_report)

    try:
        data_quality_report.to_csv(f"{OUTPUT_PATH}data_quality_report.csv", index=False)
    except Exception as e:
        logger.error(f"An error occurred while writing the data quality report: {e}")
        sys.exit(1)
    else:
        logger.info("Data quality report written successfully")

    logger.info("Data quality engine completed successfully")


if __name__ == "__main__":
    main()
