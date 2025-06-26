# Extraxt data from BigQuery and save it to Parquet files
# Run this script from root to read .env file and interpret data path correctly

import logging
import os

from dotenv import load_dotenv
from google.cloud import bigquery

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Load environment variables
load_dotenv()
logging.info("Environment variables loaded")

DATASET_ID = os.getenv("BIGQUERY_DATASET")
if not DATASET_ID:
    logging.error("BIGQUERY_DATASET environment variable not set")
    exit(1)

RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
if not RAW_DATA_PATH:
    logging.error("RAW_DATA_PATH environment variable not set")
    exit(1)

# Create BigQuery client
client = bigquery.Client()
logging.info("BigQuery client created")

# Save BigQuery dataset tables to local Parquet files
try:
    dataset = client.get_dataset(DATASET_ID)
    logging.info("Dataset ID: %s", dataset.dataset_id)
    logging.info("Location: %s", dataset.location)
    logging.info("Downloading tables to Parquet files...")
    tables = list(client.list_tables(dataset))
    for table_item in tables:
        table = client.get_table(table_item.reference)
        mb_size = table.num_bytes / 1024 ** 2
        # Download table to DataFrame
        df = client.list_rows(table).to_dataframe()
        # Save DataFrame to Parquet file
        parquet_file = RAW_DATA_PATH + f"{table.table_id}.parquet"
        df.to_parquet(parquet_file, index=False)
        logging.info("Saved %s (%i rows, %.2f MB)", table.table_id, table.num_rows, mb_size)
except Exception as e:
    logging.error("Failed to extract dataset: %s", e)
    exit(1)
