import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import time
from job_features import (
	get_experience_level,
	get_skills,
	get_role_categories,
	get_state,
	get_city,
	safe_parse,
	build_dedup_key)


load_dotenv()

RAPID_API_KEY = os.getenv("rapidapi_key")
adz_key = os.getenv("adz_key")
adz_id = os.getenv("adz_id")
print(RAPID_API_KEY)

class ETL():
	def __init__(self):
		super().__init__()
		self.connection = psycopg2.connect(
			host="localhost",
			database="Job_platform",
			user="postgres",
			password="Intention2025%",
			port="5432"
		)

		cursor = self.connection.cursor()

	def extract_jsearch(self):
		all_jobs = []
		querys = ["Data Engineer in Canada",
    			  "Machine Learning Engineer in Canada",
    			  "AI Engineer in Canada",
				  "Backend Engineer in Canada",
				  "Python Developer in Canada",
				  "Data Scientist in Canada",
				  "MLOps Engineer in Canada",
				  "Analytics Engineer in Canada",
				  "Cloud Engineer in Canada",
				  "Data Analyst in Canada"]

		url = "https://jsearch.p.rapidapi.com/search-v2"

		headers = {
			"x-rapidapi-key": RAPID_API_KEY,
			"x-rapidapi-host": "jsearch.p.rapidapi.com",
			"Content-Type": "application/json"
		}

		for query in querys:
			querystring = {"query": query, "num_pages": "3", "country": "ca", "date_posted": "week"}

			response = requests.get(url, headers=headers, params=querystring)


			while response.status_code == 429:
				print("Rate limited. Sleeping...")
				time.sleep(5)
				response = requests.get(url, headers=headers, params=querystring)
				print("response status:", response.status_code)
			time.sleep(2)

			data = response.json().get("data", {})
			jobs = data.get("jobs", [])
			print("length of job",len(jobs))
			all_jobs.extend(jobs)


		df = pd.DataFrame(all_jobs)
		return df

	def extract_adzuna(self):
		url = "https://api.adzuna.com/v1/api/jobs/ca/search/1"

		all_jobs = []
		queries = ["Data Engineer",
				   "Machine Learning Engineer",
				   "AI Engineer",
				   "Backend Engineer",
				   "Python Developer",
				   "Data Scientist",
				   "MLOps Engineer",
				   "Analytics Engineer",
				   "Cloud Engineer",
				   "Data Analyst"]

		for query in queries:
			params = {
				"app_id": adz_id,
				"app_key": adz_key,
				"what": query,
				"where": "Canada",
				"results_per_page": 50,
				"content-type": "application/json"
			}

			response = requests.get(url, params=params)

			while response.status_code == 429:
				print("Rate limited. Sleeping...")
				time.sleep(5)
				response = requests.get(url, params=params)
				print("response status:", response.status_code)
			time.sleep(2)

			data = response.json()
			jobs = data.get("results", [])
			print("length of job_adz", len(jobs))
			all_jobs.extend(jobs)

		df_adzuna = pd.DataFrame(all_jobs)
		return df_adzuna


	def transform_jsearch(self, df):
		if df.empty:
			return df

		df.columns = df.columns.str.strip()

		columns = [
			"job_id",
			"job_title",
			"employer_name",
			"job_country",
			"job_city",
			"job_state",
			"job_is_remote",
			"job_posted_at_datetime_utc",
			"job_description"
		]

		df = df[[c for c in columns if c in df.columns]]

		df["source"] = "jsearch"

		df = df.dropna(subset=["job_id", "job_title"])

		df["job_country"] = df["job_country"].str.upper()

		df = df[df["job_country"].isin(["CA", "CAN"])]

		df["job_city"] = df["job_city"].fillna("Unknown")
		df["job_state"] = df["job_state"].fillna("Unknown")

		df["job_is_remote"] = df["job_is_remote"].fillna(0)

		df = df.drop_duplicates(subset="job_id")

		return df

	def transform_adzuna(self, df_adzuna):
		if df_adzuna.empty:
			return df_adzuna

		df_adzuna["company"] = df_adzuna["company"].apply(safe_parse)
		df_adzuna["location"] = df_adzuna["location"].apply(safe_parse)

		df_clean = pd.DataFrame()

		df_clean["job_id"] = df_adzuna["id"]
		df_clean["job_title"] = df_adzuna["title"]
		df_clean["employer_name"] = df_adzuna["company"].apply(lambda x: x.get("display_name", "Unknown"))
		df_clean["job_state"] = df_adzuna["location"].apply(get_state)
		df_clean["job_city"] = df_adzuna["location"].apply(get_city)
		df_clean["job_posted_at_datetime_utc"] = df_adzuna["created"]
		df_clean["job_description"] = df_adzuna["description"]
		df_clean["job_country"] = "CA"
		df_clean["job_is_remote"] = 0
		df_clean["source"] = "adzuna"

		df_clean = df_clean.drop_duplicates(subset="job_id")

		return df_clean

	def transform(self, df):
		if df.empty:
			return df

		df = df.drop_duplicates()

		df["dedup_key"] = df.apply(build_dedup_key, axis=1)
		df = df.drop_duplicates(subset=["dedup_key"])

		df["job_is_remote"] = df["job_is_remote"].fillna(0).apply(lambda x: bool(int(x)))

		df["ingestion_time"] = pd.Timestamp.utcnow().isoformat()

		df["job_description"] = df["job_description"].fillna("")


		# Experience Level
		df["experience_level"] = df.apply(
			lambda row: get_experience_level(row.get("job_title", ""),
											 row.get("job_description", "")), axis=1
		)

		# skills column
		df["skills"] = df.apply(
			lambda row: get_skills(row.get("job_title", ""),
								   row.get("job_description", "")),
			axis=1
		)

		# skills count
		df["skills_count"] = df["skills"].apply(
			lambda x: 0 if x == ["unknown"] else len(x)
		)

		# role_category
		df["role_category"] = df.apply(
			lambda row: get_role_categories(row.get("job_title", ""), row.get("job_description", "")),
			axis=1
		)

		df["skills"] = df["skills"].apply(
			lambda x: ", ".join(x) if isinstance(x, list) else x
		)

		return df


	def load(self, df):

		if df.empty:
			print("No data to load")
			return

		cursor = self.connection.cursor()

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
			   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			   ON CONFLICT (dedup_key) DO NOTHING
			   """

		rows = df.to_records(index=False)

		execute_values(cursor, insert_query, rows)

		self.connection.commit()
		print(f"Inserted {len(rows)} new rows")