# Script to generate profile reports for all tables of theLook

import logging
import os

import pandas as pd
import yaml
from dotenv import load_dotenv
from ydata_profiling import ProfileReport

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Get filepaths from environment variables
load_dotenv()
logging.info("Environment variables loaded")

RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
if not RAW_DATA_PATH:
    logging.error("RAW_DATA_PATH environment variable not set")
    exit(1)

SOURCES_PATH = os.getenv("SOURCES_PATH")
if not SOURCES_PATH:
    logging.error("SOURCES_PATH environment variable not set")
    exit(1)

PROFILES_PATH = os.getenv("PROFILES_PATH")
if not PROFILES_PATH:
    logging.error("PROFILES_PATH environment variable not set")
    exit(1)

# Helper function to parse table and column info from sources.yml
def parse_dbt_sources(filepath):
    """
    Parse dbt sources.yml file and extract tables, columns, and semantic types.

    Returns:
        List of dictionaries with:
        - table (str): table name
        - columns (list of dict): each with 'column', 'semantic_type'
    """
    with open(filepath) as f:
        data = yaml.safe_load(f)

    source = data["sources"][0]  # Assumes only one source - theLook

    result = []

    for table in source["tables"]:
        table_name = table["name"]
        columns = []

        for col in table.get("columns", []):
            col_name = col["name"]
            semantic_type = col.get("meta", {}).get("semantic_type", "not_set")

            columns.append({
                "name": col_name,
                "semantic_type": semantic_type
            })

        result.append({
            "name": table_name,
            "columns": columns
        })

    return result

# Load data
source = parse_dbt_sources(SOURCES_PATH)
dfs = {}
for table in source:
    table_name = table["name"]
    parquet_file = os.path.join(RAW_DATA_PATH, f"{table_name}.parquet")

    if not os.path.exists(parquet_file):
        logging.error(f"Parquet file for table {table_name} does not exist")
        continue

    logging.info(f"Loading data for table: {table_name}")
    df = pd.read_parquet(parquet_file)

    # Apply manual types based on semantic_type
    for col in table["columns"]:
        if col["semantic_type"] == "categorical":
            df[col["name"]] = df[col["name"]].astype("category")

    dfs[table_name] = df

# Create profile reports
for name, df in dfs.items():
    logging.info(f"Generating profile report for table: {name}")
    profile = ProfileReport(df, title=f"Profile Report for {name}")
    report_file = os.path.join(PROFILES_PATH, f"{name}_profile.html")
    profile.to_file(report_file)
    logging.info(f"Profile report saved to: {report_file}")

logging.info("Profile reports generated for all tables.")
