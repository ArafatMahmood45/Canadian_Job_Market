import pandas as pd
import sqlite3
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs_ca_new (
    job_id TEXT,
    job_title TEXT,
    employer_name TEXT,
    job_country TEXT,
    job_city TEXT,
    job_state TEXT,
    job_is_remote INTEGER,
    job_posted_at_datetime_utc TEXT,
    job_description TEXT,
    experience_level TEXT,
    skills TEXT,
    skills_count INTEGER,
    role_category TEXT,
    source TEXT,
    dedup_key TEXT UNIQUE,
    ingestion_time TEXT
    )
    """)

cursor.execute("""
INSERT INTO jobs_ca_new (
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
SELECT
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
FROM jobs_ca
"""
)

connection.commit()
connection.close()
