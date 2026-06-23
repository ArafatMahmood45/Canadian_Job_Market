import psycopg2
from sqlalchemy import create_engine
import sqlite3
from psycopg2.extras import execute_values
import pandas as pd
#
# lite_connection = sqlite3.connect("data.db")
# cursor_lite = lite_connection.cursor()
#
# pg_connection = psycopg2.connect(
#     host="localhost",
#     database="Job_platform",
#     user="postgres",
#     password="Intention2025%",
#     port="5432"
# )
# pg_cursor = pg_connection.cursor()
#
# cursor_lite.execute("SELECT * FROM jobs_ca_new")
# rows = cursor_lite.fetchall()
#
# convert_row = []
#
# for row in rows:
#     row = list(row)
#     row[6] = bool(row[6])
#     convert_row.append(tuple(row))
#     convert_row.append(tuple(row))
#
# insert_query = """
# INSERT INTO jobs_ca (
#     job_id,
#     job_title,
#     employer_name,
#     job_country,
#     job_city,
#     job_state,
#     job_is_remote,
#     job_posted_at_datetime_utc,
#     job_description,
#     experience_level,
#     skills,
#     skills_count,
#     role_category,
#     source,
#     dedup_key,
#     ingestion_time
# )
# VALUES %s
# ON CONFLICT (dedup_key) DO NOTHING
#     """
#
# execute_values(pg_cursor, insert_query, convert_row)
#
# pg_connection.commit()
#
# lite_connection.close()
# pg_connection.close()

connection1 = psycopg2.connect(
    host="localhost",
    database="Job_platform",
    user="postgres",
    password="Intention2025%",
    port="5432"
)

df = pd.read_sql("SELECT * FROM jobs_ca", connection1)
print(df)

engine2 = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5433/postgres"
)

df.to_sql("jobs_ca_new", engine2, if_exists="replace", index=False)

print("Connected and table passed!")
