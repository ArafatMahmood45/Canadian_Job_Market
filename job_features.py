import pandas as pd
import sqlite3

connection = sqlite3.connect('data.db')

df = pd.read_sql("SELECT * FROM jobs_ca", connection)

# #remove job_description & job_country: not needed for dashboard analysis
# df = df.drop(["job_country"], axis=1)
title = df.job_title
description = df.job_description

#create experience level column
def get_experience_level(title, description):
    text = f'{title} {description}'.lower()

    entry_keywords = [
        "entry level", "junior", "jr", "new grad", "new graduate",
        "graduate", "intern", "internship", "no experience",
        "0-1 year", "0–1 year", "0 to 1 year"
    ]

    senior_keywords = [
        "senior", "sr", "lead", "principal", "architect",
        "5+ years", "8+ years", "7+ years", "10+ years"
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

# create skills column
def get_skills(title, description):
    text = f'{title} {description}'.lower()
    skills_list = [
        # Programming
        "python", "r", "sql", "bash", "java", "c++", "javascript",

        # Data Engineering
        "pandas", "numpy", "etl", "elt", "spark", "pyspark",
        "airflow", "dbt", "databricks", "snowflake", "kafka",
        "data pipeline", "data warehouse", "data lake",

        # ML / AI
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "nlp", "computer vision", "llm",
        "transformers", "mlops",

        # Cloud / DevOps
        "aws", "azure", "gcp", "docker", "kubernetes",
        "terraform", "ci/cd", "jenkins",

        # Analytics
        "excel", "power bi", "tableau", "looker",
        "data visualization", "statistics", "a/b testing",

        # Backend
        "backend", "api", "rest api", "flask", "fastapi", "django"
    ]

    skill_found = []
    for skills in skills_list:
        if skills in text:
            skill_found.append(skills)

    return list(set(skill_found)) if skill_found else ["unknown"]


df["skills"] = df.apply(
    lambda row: get_skills(row.get("job_title", ""),row.get("job_description", "")), axis=1
)

df["skills_count"] = df["skills"].apply(
    lambda x: 0 if x == ["unknown"] else len(x)
)

print(df["skills"].explode().value_counts())

#create role category column
role_categories = {
    "Data Engineering": [
        "data engineer",
        "etl developer",
        "analytics engineer",
        "data platform",
        "data pipeline"
    ],

    "Machine Learning": [
        "machine learning",
        "ml engineer",
        "ai engineer",
        "mlops",
        "computer vision",
        "nlp"
    ],

    "Data Science": [
        "data scientist",
        "research scientist",
        "applied scientist"
    ],

    "Backend Engineering": [
        "backend engineer",
        "python developer",
        "software engineer",
        "backend developer"
    ],

    "Cloud/Infrastructure": [
        "cloud engineer",
        "devops",
        "site reliability",
        "infrastructure engineer"
    ]
}

def get_role_categories(title):
    text = f'{title}'.lower()

    for category, keywords in role_categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "unknown"

df["role_category"] = df.apply(
    lambda row: get_role_categories(row.get("job_title", "")), axis=1
)

df_exploded = df[['job_id', 'skills']].explode('skills')
df_exploded = df_exploded.rename(columns={'skills': 'skill'})

df_jobs = df.copy(deep=True)
df_jobs["skills"] = df_jobs["skills"].apply(lambda x: ", ".join(x))

#df_jobs.to_sql("jobs_ca", connection, if_exists="replace", index=False)
#df_exploded.to_sql("jobs_skills", connection, if_exists="replace", index=False)

print(df)
