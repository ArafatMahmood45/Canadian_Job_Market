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
print(jobs.columns)

import ast

df["company"] = df["company"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else {})
df["location"] = df["location"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else {})


