# Sitelucent_Assignment
# Currency Conversion Rates ETL and Reporting

This repository contains a Python-based ETL pipeline and reporting solution for currency conversion rates. It includes scripts to fetch, process, and store currency conversion rates from an external API into a MySQL database. It also includes SQL scripts to set up the database schema and generate reports.

## Project Overview

1. **Data Fetching**: Python scripts fetch daily conversion rates from [FloatRates API](https://www.floatrates.com/json-feeds.html).
2. **Data Storage**: Conversion rates are stored in a MySQL database.
3. **Reporting**: Generate rolling 7-day conversion rate charts

## Table of Contents

- [Setup and Installation](#setup-and-installation)
- [Python Scripts](#python-scripts)
- [SQL Scripts](#sql-scripts)
- [Running the ETL Pipeline](#running-the-etl-pipeline)
- [Generating Reports](#generating-reports)



## Setup and Installation

### Prerequisites

- Python 3.x
- MySQL Server
- MySQL Connector
- Power BI (for reporting)

### Install Required Python Packages

Install the necessary Python libraries using pip:

```bash
pip install pyodbc sqlalchemy pandas requests schedule mysql-connector-python
```

### Set Up the MySQL Database

1. **Create the Database**: Create a MySQL database to hold the currency data.

2. **Run SQL Scripts**: Execute the SQL scripts provided in the `sql` directory to create tables and set up indices.

## Python Scripts

### 1. `fetch_conversion_rates.py`

This script fetches daily conversion rates from the FloatRates API and saves them to CSV files. It also saves the CSV data into the MySQL database.

**Functions**:
- `fetch_conversion_rates(Url)`: Fetches conversion rates from a given URL.
- `dump_to_csv(df, currency)`: Saves DataFrame to a CSV file.
- `fetch_conversion_dump_to_csv()`: Fetches and saves conversion rates for multiple currencies.

### 2. `persist_csv_to_db.py`

This script handles the database interactions to store the CSV data.

**Functions**:
- `loadCurrencyTableData(session, table)`: Loads currency reference data from the database.
- `createEntryForCsvFile(csv_path, session, csvTable)`: Records the CSV file details in the database.
- `checkInMap(key_value_pairs, val)`: Checks and retrieves currency ID from the reference map.
- `save_csv_to_db(csv_path, mainCurrencyCode)`: Saves CSV data into the MySQL database.

### 3. `daily_task_scheduler.py`

This script schedules the ETL pipeline to run daily at 14:00.

**Features**:
- Uses `schedule` library to run the `fetch_conversion_dump_to_csv()` function daily.

## SQL Scripts

### `database_setup.sql`

SQL script to set up the database schema.

**Tables Created**:
- `REF_CURRENCY`
- `CSV_FILE`
- `CURRENCY_CONVERSION_RATES`

**Indices**:
- Index on `CURRENCY_CODE` in `REF_CURRENCY`
- Index on `CSV_FILE_ID` in `CURRENCY_CONVERSION_RATES`

## Running the ETL Pipeline

1. **Configure the Database Connection**: Update the `DATABASE_URL` in `persist_csv_to_db.py` with your MySQL connection details.

2. **Run Daily Task Scheduler**:
   ```bash
   python daily_task_scheduler.py
   ```

   This will schedule the ETL process to run daily at 14:00.

## Generating Reports

To generate reports and visualize the data:

1. **Use Power BI**:
   - Connect Power BI to your MySQL database.
   - Import the tables `REF_CURRENCY` and `CURRENCY_CONVERSION_RATES`.
   - Create visuals and reports using Power BI's features.



