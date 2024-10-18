# Data Quality Rule Engine

## Introduction

The Data Quality Rule Engine is a tool that allows users to define and execute data quality rules on a dataset. The tool is designed to be flexible and extensible, allowing users to define their own rules and apply them to their data.

## How to use

1. Add your data to the `data` folder, in CSV format.

2. Define your rules in the `rules` folder, in YAML format.

   - Each rule should be its own yaml file.
   - Each rule should have a `name`, `query`, `error_message`, and `dimension` field.
   - The `query` field should be a Pandas query string that will be applied to the dataset.
   - The `error_message` field should be a string that will be displayed if the rule fails.
   - The `dimension` field should be a string that will be used to group the results (e.g. "Completeness", "Validity", etc.).

   Example rule:

   ```yaml
   name: "Check for missing values"
   query: "column_name.isnull().any()"
   error_message: "Missing values found in column_name"
   dimension: "Completeness"
   ```

3. Define your schema in the `schema` folder, in YAML format.

   - Each schema should be its own yaml file that corresponds to the dataset.
   - Each schema should have a `name`, `filename`, `source_system`, `business_unit`, `data_owner`, `data_steward`, `data_classification`, and `columns` field.
   - The `name` field should be the name of the dataset.
   - The `filename` field should be the name of the CSV file that contains the data.
   - The `source_system` field should be the name of the system that the data comes from.
   - The `business_unit` field should be the name of the business unit that owns the data.
   - The `data_owner` field should be the name of the person who owns the data.
   - The `data_steward` field should be the name of the person who is responsible for the data quality.
   - The `data_classification` field should be the classification of the data (e.g. PII, Internal, PCI, etc.).
   - The `columns` field should be a list of column names in the dataset.

   Example schema:

   ```yaml
   name: "Sales"
   filename: "sales.csv"
   source_system: "Microsoft Dynamics CRM"
   business_unit: "Sales"
   data_owner: "John Doe"
   data_steward: "Jane Doe"
   data_classification: "PII"
   columns:
     - name: "first_name"
       data_type: "string"
       data_classification: "PII"
     - name: "last_name"
       data_type: "string"
       data_classification: "PII"
     - name: "email"
       data_type: "string"
       data_classification: "PII"
     - name: "phone_number"
       data_type: "string"
       data_classification: "PII"
   ```

4. Run the `scripts/run.sh` script to execute the rules on the dataset.

   - The script will generate a report in the `output` folder that shows the results of the rules.

## Example

An example dataset, rules, and schema are provided in the `data`, `rules`, and `schema` folders, respectively. You can run the example by running the `scripts/run.sh` script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
