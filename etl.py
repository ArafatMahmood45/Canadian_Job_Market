import requests
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("rapidapi-key")

class ETL():
	def __init__(self):
		super().__init__()
		self.connection = sqlite3.connect("data.db")

		cursor = self.connection.cursor()

		cursor.execute("""
		        CREATE TABLE IF NOT EXISTS jobs_ca (
		            job_id TEXT PRIMARY KEY,
		            job_title TEXT,
		            employer_name TEXT,
		            job_country TEXT,
		            job_city TEXT,
		            job_state TEXT,
		            job_is_remote INTEGER,
		            job_posted_at_datetime_utc TEXT,
		            job_description TEXT
		        )
		        """)

		self.connection.commit()

	def extract(self):
		all_jobs = []
		querys = ["Data Engineer in Canada",
    			  "Machine Learning Engineer in Canada",
    			  "AI Engineer in Canada",
				  "Backend Engineer in Canada",
				  "Python Developer in Canada",
				  "Data Scientist in Canada",
				  "MLOps Engineer in Canada",
				  "Analytics Engineer in Canada",
				  "Cloud Engineer in Canada"]

		url = "https://jsearch.p.rapidapi.com/search-v2"

		headers = {
			"x-rapidapi-key": API_KEY,
			"x-rapidapi-host": "jsearch.p.rapidapi.com",
			"Content-Type": "application/json"
		}

		for query in querys:
			querystring = {"query": query, "num_pages": "3", "country": "ca", "date_posted": "week"}

			response = requests.get(url, headers=headers, params=querystring)
			print("response status:",response.status_code)
			print("json response", response.json())

			data = response.json().get("data", {})
			jobs = data.get("jobs", [])
			print("length of job",len(jobs))
			all_jobs.extend(jobs)

		df = pd.DataFrame(all_jobs)
		return df

	def transform(self, df):
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

		df = df.dropna(subset=["job_id", "job_title"])

		df["job_country"] = df["job_country"].str.upper()

		df = df[df["job_country"].isin(["CA", "CAN"])]

		df["job_city"] = df["job_city"].fillna("Unknown")
		df["job_state"] = df["job_state"].fillna("Unknown")

		df["job_is_remote"] = df["job_is_remote"].fillna(0)

		df = df.drop_duplicates(subset="job_id")

		return df


	def load(self, df):

		if df.empty:
			print("No data to load")
			return

		cursor = self.connection.cursor()

		inserted = 0
		for _, row in df.iterrows():
			cursor.execute("""
			   INSERT OR IGNORE INTO jobs_ca (
				   job_id,
				   job_title,
				   employer_name,
				   job_country,
				   job_city,
				   job_state,
				   job_is_remote,
				   job_posted_at_datetime_utc,
				   job_description
			   )
			   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
			   """, (
				row.get("job_id"),
				row.get("job_title"),
				row.get("employer_name"),
				row.get("job_country"),
				row.get("job_city"),
				row.get("job_state"),
				row.get("job_is_remote"),
				row.get("job_posted_at_datetime_utc"),
				row.get("job_description")
			))

			if cursor.rowcount > 0:
				inserted += 1

		self.connection.commit()

		print(f"Inserted {inserted} new rows")






