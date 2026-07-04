import psycopg2
from sqlalchemy import create_engine
import pandas as pd

connection = psycopg2.connect(
    host="localhost",
    database="Job_platform",
    user="postgres",
    password="Intention2025%",
    port="5432"
)

df = pd.read_sql("SELECT * FROM jobs_ca", connection)
print(df)

engine2 = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5433/postgres"
)

df.to_sql("jobs_ca_new", engine2, if_exists="replace", index=False)

print("Connected and table passed!")
