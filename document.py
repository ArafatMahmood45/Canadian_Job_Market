import psycopg2
from pgvector.psycopg2 import register_vector
from openai import OpenAI
import pandas as pd
from etl import pg_password
from etl import openai_key

client = OpenAI(api_key=openai_key)

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password=pg_password,
    port="5433"
)

cur = connection.cursor()
register_vector(connection)

df = pd.read_sql("""
    SELECT job_id, job_title, employer_name, job_city, job_state,
           job_country, job_is_remote, role_category,
           experience_level, skills, job_description
    FROM jobs_ca_new
    WHERE embedding IS NULL
""", connection)

def safe(x):
    return "Not specified" if pd.isna(x) or x == "" else str(x)

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

def get_embeddings(texts):
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    ).data

df["document"] = df.apply(create_document, axis=1)

results = get_embeddings(df["document"].tolist())
embeddings = [r.embedding for r in results]

for i, row in df.iterrows():
    cur.execute("""
        UPDATE jobs_ca
        SET embedding = %s
        WHERE id = %s
    """, (embeddings[i], row["id"]))

connection.commit()

# query = "python machine learning engineer remote Canada"
#
# query_embedding = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=query
# ).data[0].embedding