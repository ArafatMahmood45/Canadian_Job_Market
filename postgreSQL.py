import psycopg2
from psycopg2.extras import execute_values

self.connection = psycopg2.connect(
    host="localhost",
    database="canada_jobs",
    user="postgres",
    password="your_password",
    port="5432"
)

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs_ca (
    job_id TEXT,
    job_title TEXT,
    employer_name TEXT,
    job_country TEXT,
    job_city TEXT,
    job_state TEXT,
    job_is_remote BOOLEAN,
    job_posted_at_datetime_utc TIMESTAMP,
    job_description TEXT,
    experience_level TEXT,
    skills TEXT,
    skills_count INTEGER,
    role_category TEXT,
    source TEXT,
    dedup_key TEXT UNIQUE,
    ingestion_time TIMESTAMP
)
""")

cursor.execute("""
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
VALUES (
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
)
ON CONFLICT (dedup_key) DO NOTHING
""", (
    row.get("job_id"),
    row.get("job_title"),
    row.get("employer_name"),
    row.get("job_country"),
    row.get("job_city"),
    row.get("job_state"),
    row.get("job_is_remote"),
    row.get("job_posted_at_datetime_utc"),
    row.get("job_description"),
    row.get("experience_level"),
    row.get("skills"),
    row.get("skills_count"),
    row.get("role_category"),
    row.get("source"),
    row.get("dedup_key"),
    row.get("ingestion_time")
))