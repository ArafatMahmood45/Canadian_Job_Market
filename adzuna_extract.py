import requests
from dotenv import load_dotenv
import os
import time
import pandas as pd

# load_dotenv()
#
# adz_key = os.getenv("adz_key")
# adz_id = os.getenv("adz_id")
#
# url = "https://api.adzuna.com/v1/api/jobs/ca/search/1"
#
# all_jobs = []
# queries = ["Data Engineer in Canada",
#     			  "Machine Learning Engineer",
#     			  "AI Engineer",
# 				  "Backend Engineer",
# 				  "Python Developer",
# 				  "Data Scientist",
# 				  "MLOps Engineer",
# 				  "Analytics Engineer",
# 				  "Cloud Engineer",
# 				  "Data Analyst"]
#
# for query in queries:
#     params = {
#         "app_id": adz_id,
#         "app_key": adz_key,
#         "what": query,
#         "where": "Canada",
#         "results_per_page": 50,
#         "content-type": "application/json"
#     }
#
#     response = requests.get(url, params=params)
#
#     while response.status_code == 429:
#         print("Rate limited. Sleeping...")
#         time.sleep(5)
#         response = requests.get(url, params=params)
#         print("response status:", response.status_code)
#     time.sleep(2)
#
#
#     data = response.json()
#     jobs = data.get("results", [])
#     all_jobs.extend(jobs)
#
# df = pd.DataFrame(all_jobs)
#
# print(df)
#
# df.to_csv("jobs_adz.csv")

df = pd.read_csv("jobs_adz.csv")

import sqlite3
import ast
from job_features import (get_experience_level,
                          get_skills,
                          get_role_categories)

df["company"] = df["company"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else {})
df["location"] = df["location"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else {})

df_clean = pd.DataFrame()

def get_city(location):
    area = location.get("area", [])

    if len(area) >= 3:
        return area[-1]

    return "Unknown"

def get_state(location):
    area = location.get("area", [])

    if len(area) >= 2:
        return area[-2]

    return "Unknown"




df_clean["job_id"] = df["id"]
df_clean["job_title"] = df["title"]
df_clean["employer_name"] = df["company"].apply(lambda x: x.get("display_name", "Unknown"))
df_clean["job_state"] = df["location"].apply(get_state)
df_clean["job_city"] = df["location"].apply(get_city)
df_clean["job_posted_at_datetime_utc"] = df["created"]
df_clean["job_description"] = df["description"]
df_clean["job_country"] = "CA"
df_clean["job_is_remote"] = 0
df_clean["source"] = "adzuna"

df_clean["experience_level"] = df_clean.apply(
			lambda row: get_experience_level(row.get("job_title", ""),
											 row.get("job_description", "")), axis=1
		)

# skills column
df_clean["skills"] = df_clean.apply(
    lambda row: get_skills(row.get("job_title", ""),
                           row.get("job_description", "")),
    axis=1
)

# skills count
df_clean["skills_count"] = df_clean["skills"].apply(
    lambda x: 0 if x == ["unknown"] else len(x)
)

# role_category
df_clean["role_category"] = df_clean.apply(
    lambda row: get_role_categories(row.get("job_title", ""), row.get("job_description", "")),
    axis=1
)

df_clean["skills"] = df_clean["skills"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else x
)


conn = sqlite3.connect("data.db")

STANDARD_COLUMNS = [
    "job_id",
    "job_title",
    "employer_name",
    "job_country",
    "job_city",
    "job_state",
    "job_is_remote",
    "job_posted_at_datetime_utc",
    "job_description",
    "experience_level",
    "skills",
    "skills_count",
    "role_category",
    "source"
]

df_clean = df_clean.reindex(columns=STANDARD_COLUMNS)
df_clean = df_clean.drop_duplicates("job_id")
print(df_clean["job_id"].duplicated().sum())


df_clean.to_sql("jobs_ca", con=conn, index=False, if_exists="append")