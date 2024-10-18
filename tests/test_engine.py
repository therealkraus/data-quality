# Standard library imports

# Related third party imports
import pandas as pd
import pytest

# Local application/library specific imports
from profiler import engine


@pytest.fixture
def test_rule():
    return {
        "not_null": {
            "query": "df[column].notnull()",
            "error_message": "Value is null.",
            "dimension": "Completeness",
        }
    }


@pytest.fixture
def expected_data_quality_report():
    return pd.read_csv("tests/test_files/expected_data_quality_report.csv")


def test_run_engine(test_rule, expected_data_quality_report):
    actual_data_quality_report = engine.run_engine(
        test_rule, ["tests/test_files/test_schema.yaml"], "tests/test_files/"
    )

    assert actual_data_quality_report == expected_data_quality_report.to_dict(
        orient="records"
    )
