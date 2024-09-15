import requests
import pandas as pd
import os
from datetime import datetime
from persist_csv_to_db import save_csv_to_db

URL_USD = "https://www.floatrates.com/daily/usd.json"
URL_INR = "https://www.floatrates.com/daily/inr.json"
CSV_DIRECTORY = "csv_data"

#fetch the data from URL in JSON format and create dataframe with exception handling
def fetch_conversion_rates(Url):
    try:
        response = requests.get(Url)
        response.raise_for_status()         #this raise status for success or failure and in case of failure it will skip try block execution
        data = response.json()              # to convert the string in to JSON format

        df = pd.DataFrame.from_dict(data, orient='index')       # to structure the data from JSON file
        df['date'] = datetime.now().strftime("%Y-%m-%d")        # to capture execution date and time

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# create directory and define file nomenclature
def dump_to_csv(df, currency):
    if not os.path.exists(CSV_DIRECTORY):
        os.makedirs(CSV_DIRECTORY)

    csv_path = os.path.join(CSV_DIRECTORY, f"{currency}_conversion_rates_{df['date'][0]}.csv")
    df.to_csv(csv_path, index=False)
    print(f"Data saved successfully to {csv_path}")
    return csv_path


# save the data to CSV file fetched from the URL
def fetch_conversion_dump_to_csv():
    df = fetch_conversion_rates(URL_USD)
    csv_path_usd = dump_to_csv(df, "USD")

    df = fetch_conversion_rates(URL_INR)
    csv_path_inr = dump_to_csv(df, "INR")

    save_csv_to_db(csv_path_usd, "USD")
    save_csv_to_db(csv_path_inr, "INR")
