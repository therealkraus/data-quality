# Standard imports
from pathlib import Path

# Related third party imports
import pandas as pd

# Local application/library specific imports
from profiler.config import RULES_PATH
from profiler.utils import glob_files, open_yaml


def load_rules():
    """
    Load rules from the rules directory.

    Returns:
        dict: A dictionary containing the rules.

    Example:
        {
            "rule_name": {
                "query": "data['column_name'] > 0",
                "error_message": "Column 'column_name' must be greater than 0",
                "dimension": "Column"
            }
        }
    """
    rule_paths = glob_files(RULES_PATH, "yaml")
    rules = {}
    for rule in rule_paths:
        rule_name = Path(rule).stem
        rule_content = open_yaml(rule)
        rules[rule_name] = {
            "query": rule_content.get("query"),
            "error_message": rule_content.get("error_message"),
            "dimension": rule_content.get("dimension"),
        }
    return rules


def apply_rule(df, column, rule):
    """
    Apply a rule to a column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to apply the rule to.
        column (str): The column to apply the rule to.
        rule (str): The rule to apply.

    Returns:
        pd.Series: A boolean Series indicating whether the rule was violated.

    Example:
        >>> apply_rule(data, "column_name", "data['column_name'] > 0")
    """
    return eval(rule)


def run_engine(rules: dict, schemas: list, data_path) -> list:
    """
    Run the data quality engine.

    Args:
        rules (dict): A dictionary containing the rules.
        schemas (list): A list of schema files.

    Returns:
        list: A list of dictionaries containing the data quality report.

    Example:
        [
            {
                "table": "Sales",
                "filename": "sales.csv",
                "source_system": "System A",
                "business_unit": "Finance",
                "data_owner": "John Doe",
                "data_steward": "Jane Smith",
                "data_classification": "Restricted",
                "column": "Amount",
                "column_data_classification": "Restricted",
                "data_type": "Numeric",
                "rule": "positive_values",
                "rule_query": "data['Amount'] > 0",
                "rule_description": "Column 'Amount' must be greater than 0",
                "rule_dimension": "Column",
                "total_records": 1000,
                "violations": 10
            }
    """
    data_quality_report = []
    for schema in schemas:
        schema_content = open_yaml(schema)
        tables = schema_content.get("tables")
        if not tables:
            continue

        for table in tables:
            table_name = table.get("name")

            columns = table.get("columns")
            if not columns:
                continue

            for column in columns:
                column_name = column.get("name")
                column_rules = column.get("rules")

                if not column_rules:
                    continue

                for column_rule in column_rules:
                    rule_name = column_rule.get("name")
                    rule = rules.get(rule_name)
                    if not rule:
                        continue

                    rule_query = rule.get("query")
                    data = pd.read_csv(f"{data_path}{table.get('filename')}")
                    result = apply_rule(data, column_name, rule_query)
                    total_records = len(data)
                    violations = int(
                        (~result).sum()
                    )  # summing the number of False values in the result

                    data_quality_report.append(
                        {
                            "table": table_name,
                            "filename": table.get("filename"),
                            "source_system": table.get("source_system"),
                            "business_unit": table.get("business_unit"),
                            "data_owner": table.get("data_owner"),
                            "data_steward": table.get("data_steward"),
                            "data_classification": table.get("data_classification"),
                            "column": column_name,
                            "column_data_classification": column.get(
                                "data_classification"
                            ),
                            "data_type": column.get("data_type"),
                            "rule": rule_name,
                            "rule_query": rule_query,
                            "rule_description": rule.get("error_message"),
                            "rule_dimension": rule.get("dimension"),
                            "total_records": total_records,
                            "violations": violations,
                        }
                    )

    return data_quality_report
