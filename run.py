import schedule
import time
from etl import ETL

def run_etl():
    etl = ETL()
    df = etl.extract()
    print(f"Extracted rows: {len(df)}")

    df = etl.transform(df)
    print(f"Rows after transform: {len(df)}")

    etl.load(df)
    print("ETL DONE")

schedule.every().day.at("14:54").do(run_etl)

while True:
    schedule.run_pending()
    time.sleep(60)

