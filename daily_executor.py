#pip install pyodbc
#pip install sqlalchemy
#pip install pandas
#pip install requests
#pip install schedule
#pip install mysql-connector-python
import schedule
import time

from fetch_conversion_rates import fetch_conversion_dump_to_csv

def daily_task():
    fetch_conversion_dump_to_csv()

schedule.every().day.at("14:00").do(daily_task)

while True:
    schedule.run_pending()
    time.sleep(1)
