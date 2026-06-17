import psycopg2
import sqlite3
from psycopg2.extras import execute_values

lite_connection = sqlite3.connect("data.db")
cursor_lite = lite_connection.cursor()

pg_connection = psycopg2.connect(
    host="localhost",
    database="Job_platform",
    user="postgres",
    password="Intention2025%",
    port="5432"
)
pg_cursor = pg_connection.cursor()

cursor_lite.execute("SELECT * FROM jobs_ca_new")
rows = cursor_lite.fetchall()

convert_row = []

for row in rows:
    row = list(row)
    row[6] = bool(row[6])
    convert_row.append(tuple(row))
    convert_row.append(tuple(row))

insert_query = """
INSERT INTO jobs_ca (
    job_id,
    job_title,
    employer_name,
    job_country,
    job_city,
    job_state,
    job_is_remote,
    job_posted_at_datetime_utc,
    job_description,
    experience_level,
    skills,
    skills_count,
    role_category,
    source,
    dedup_key,
    ingestion_time
)
VALUES %s
ON CONFLICT (dedup_key) DO NOTHING
    """

execute_values(pg_cursor, insert_query, convert_row)

pg_connection.commit()

lite_connection.close()
pg_connection.close()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS jobs_ca (
#     job_id TEXT,
#     job_title TEXT,
#     employer_name TEXT,
#     job_country TEXT,
#     job_city TEXT,
#     job_state TEXT,
#     job_is_remote BOOLEAN,
#     job_posted_at_datetime_utc TIMESTAMP,
#     job_description TEXT,
#     experience_level TEXT,
#     skills TEXT,
#     skills_count INTEGER,
#     role_category TEXT,
#     source TEXT,
#     dedup_key TEXT UNIQUE,
#     ingestion_time TIMESTAMP
# )
# """)
#
# connection.commit()
# cursor.close()
# connection.close()

#
# cursor.execute("""

# )
# ON CONFLICT (dedup_key) DO NOTHING
# """, (
#     row.get("job_id"),
#     row.get("job_title"),
#     row.get("employer_name"),
#     row.get("job_country"),
#     row.get("job_city"),
#     row.get("job_state"),
#     row.get("job_is_remote"),
#     row.get("job_posted_at_datetime_utc"),
#     row.get("job_description"),
#     row.get("experience_level"),
#     row.get("skills"),
#     row.get("skills_count"),
#     row.get("role_category"),
#     row.get("source"),
#     row.get("dedup_key"),
#     row.get("ingestion_time")
# ))