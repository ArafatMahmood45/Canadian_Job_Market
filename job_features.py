import pandas as pd
import sqlite3

connection = sqlite3.connect('data.db')

df = pd.read_sql("SELECT * FROM jobs_ca", connection)

#remove job_description & job_country: not needed for dashboard analysis
df = df.drop(["job_country"], axis=1)
title = df.job_title
description = df.job_description


def get_experience_level(title, description):
    text = f'{title} {description}'.lower()

    entry_keywords = [
        "entry level", "junior", "jr", "new grad", "new graduate",
        "graduate", "intern", "internship", "no experience",
        "0-1 year", "0–1 year", "0 to 1 year"
    ]

    senior_keywords = [
        "senior", "sr", "lead", "principal", "architect",
        "5+ years", "7+ years", "10+ years"
    ]


    if any(word in text for word in entry_keywords):
        return "entry"

    if any(word in text for word in senior_keywords):
        return "senior"

    return "unknown"

df["experience_level"] = df.apply(
    lambda row: get_experience_level(row.get("job_title", ""),
                                     row.get("job_description", "")), axis=1
)
print(df[df["experience_level"] == "unknown"]["job_description"].head())





