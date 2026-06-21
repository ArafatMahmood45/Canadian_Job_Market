import psycopg2
from etl import pg_password
import pandas as pd
from openai import OpenAI

client = OpenAI()
#
# connection = psycopg2.connect(user="postgres", database="Job_platform", password=pg_password, host="localhost", port="5432")
#
# df = pd.read_sql("SELECT * FROM jobs_ca", connection)
#
# df.to_csv("document.csv")

df = pd.read_csv("document.csv")
df = df.drop('Unnamed: 0', axis=1)

def safe(x):
    if pd.isna(x) or x == "":
        return "Not specified"
    return str(x)

def create_document(row):
    return f"""
Job Title: {safe(row['job_title'])}
Company: {safe(row['employer_name'])}
Location: {safe(row['job_city'])}, {safe(row['job_state'])}, {safe(row['job_country'])}
Remote: {safe(row['job_is_remote'])}
Role Category: {safe(row['role_category'])}
Experience Level: {safe(row['experience_level'])}
Skills: {safe(row['skills'])}

Job Description:
{safe(row['job_description'])}
""".strip()

df["document"] = df.apply(create_document, axis=1)

print(df.head())



def get_embedding(text):
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

df["embedding"] = df["document"].apply(get_embedding)



