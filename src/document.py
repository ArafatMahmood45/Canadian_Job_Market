from sqlalchemy import text
from openai import OpenAI
import pandas as pd
from src.config import OPENAI_API_KEY
from src.database import engine

print("SCRIPT STARTED")

client = OpenAI(api_key=OPENAI_API_KEY)

engine = engine

df = pd.read_sql("""
    SELECT job_id, job_title, employer_name, job_city, job_state,
           job_country, job_is_remote, role_category,
           experience_level, skills, job_description
    FROM jobs_ca_new
    WHERE embedding IS NULL
""", engine)

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

df["document"] = df.apply(create_document, axis=1)

BATCH_SIZE = 100
all_embeddings = []

for i in range(0, len(df), BATCH_SIZE):
    batch = df["document"].tolist()[i:i + BATCH_SIZE]

    results = client.embeddings.create(
        model="text-embedding-3-small",
        input=batch
    ).data

    batch_embeddings = [r.embedding for r in results]

    # STRICT CHECK (important fix)
    if len(batch_embeddings) != len(batch):
        raise ValueError(f"Batch {i} mismatch: expected {len(batch)}, got {len(batch_embeddings)}")

    all_embeddings.extend(batch_embeddings)

# FINAL SAFETY CHECK (IMPORTANT FIX)
if len(all_embeddings) != len(df):
    raise ValueError(
        f"Embedding mismatch: df={len(df)} embeddings={len(all_embeddings)}"
    )

print("df:", len(df))
print("embeddings:", len(all_embeddings))

print("None embeddings:", sum(x is None for x in all_embeddings))

with engine.begin() as conn:
    conn.execute(
        text("""
            UPDATE jobs_ca_new
            SET embedding = :embedding
            WHERE job_id = :job_id
        """),
        [
            {"job_id": job_id, "embedding": emb}
            for job_id, emb in zip(df["job_id"].tolist(), all_embeddings)
        ]
    )