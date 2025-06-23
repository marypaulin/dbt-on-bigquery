# Data Engineering Project: Transforming eCommerce data for Inventory Optimization using dbt on BigQuery

<span style="color:purple"><em>👾 Under construction 👾</em></span>

This project showcases a modern data modeling task using dbt on Google BigQuery to support inventory optimization use cases on sample eCommerce data.

It aims to be part of a larger ELT pipeline and focuses exclusively on the **transform** layer, to be integrated into an Airflow-orchestrated pipeline later.

## Data

This project uses the synthetic **theLook eCommerce** dataset, publicly available in Google BigQuery. It includes sales, customer, and inventory data. Key tables are:

- `orders`: Sales transactions, including dates, order value, and profit
- `order_items`: Line items for each order, includes quantity and product linkage
- `products`: Product catalog with category, brand, and price info
- `users`: Customer demographic info (gender, age, location)
- `distribution_centers`: Info on where products are shipped from
- `inventory_items`: Inventory status per product per location

These serve as the raw sources for dbt transformations. The Entity Relationship Diagram (ERD) for this dataset looks as follows (listing fewer columns for readability):

![ERD Diagram](data/theLook_eCommerce_ERD_red.png)

## Use Cases

The dbt models are designed to support inventory optimization efforts. Handled use cases include:

TBD

## Tools

This project uses

- dbt-bigquery (for transformations)
- jupyter, pandas, matplotlib (for EDA)

## dbt Structure

This project will follow standard dbt best practices:

- **Staging models**: source-specific, lightly cleaned tables (`stg_`)
- **Intermediate models**: business logic and joins (`int_`)
- **Mart models**: final analytical tables, ready for consumption (`mart_`)
- **Tests**: data quality checks to ensure model integrity

## Setup

To run this project:

TBD

## Testing

This project will include built-in dbt tests:

TBD
