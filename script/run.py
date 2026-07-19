import schedule
import time
from src.etl import ETL
import pandas as pd

def run_etl():
    etl = ETL()
    df_adzuna = etl.extract_adzuna()
    #df_jsearch =etl.extract_jsearch()

    df_adzuna = etl.transform_adzuna(df_adzuna)
    #df_jsearch = etl.transform_jsearch(df_jsearch)

    #new - remove later
    df = df_adzuna
    df = df.drop_duplicates(subset=["job_id"])

    # df = pd.concat([df_adzuna, df_jsearch], ignore_index=True)
    # df = df.drop_duplicates(subset=["job_id"])

    df = etl.transform(df)
    print(f"Rows after transform: {len(df)}")

    etl.load(df)
    print("ETL DONE")

schedule.every().day.at("23:22").do(run_etl)

while True:
    schedule.run_pending()
    time.sleep(60)

