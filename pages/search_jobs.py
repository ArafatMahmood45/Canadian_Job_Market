import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI
from etl import openai_key

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Search Jobs",
    layout="wide"
)

st.title("Search Jobs (Canada Job Market)")

st.subheader("AI Semantic Job Search")

st.info(
    """
    🤖 Describe the job you're looking for in natural language.

    Examples:
    - Entry-level AI jobs in Toronto
    - Remote Python developer jobs with SQL
    - Machine learning roles for new graduates
    """
)

# =========================
# INPUT
# =========================
semantic_query = st.text_area(
    "Describe the job you're looking for",
    placeholder="Example: Entry-level AI job in Toronto with Python and machine learning"
)

search_button = st.button("Search")

# =========================
# OPENAI CLIENT
# =========================

api_key = openai_key
client = OpenAI(api_key=api_key)

# =========================
# DATABASE CONNECTION (POSTGRES)
# =========================
engine = create_engine(
    "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5433/postgres"
)

# =========================
# LOAD DATA (WITH EMBEDDINGS)
# =========================
jobs = pd.read_sql(
    """
    SELECT job_id, job_title, employer_name, job_city, job_state,
           job_country, job_is_remote, role_category,
           experience_level, skills, job_description
    FROM jobs_ca_new
    """,
    engine
)

jobs["skills"] = jobs["skills"].fillna("unknown")

# =========================
# SIDEBAR FILTERS
# =========================
st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:
    role_filter = st.selectbox(
        "Role Category",
        ["All"] + sorted(jobs["role_category"].dropna().unique())
    )

with col2:
    province_filter = st.selectbox(
        "Province",
        ["All"] + sorted(jobs["job_state"].dropna().unique())
    )

with col3:
    experience_filter = st.selectbox(
        "Experience Level",
        ["All"] + sorted(jobs["experience_level"].dropna().unique())
    )

col4, col5 = st.columns(2)

with col4:
    remote_filter = st.selectbox(
        "Work Type",
        ["All", "Remote", "On-Site"]
    )

with col5:
    keyword = st.text_input("Search Job Title")

# =========================
# SKILLS FILTER
# =========================
all_skills = (
    jobs["skills"]
    .str.split(", ")
    .explode()
    .dropna()
    .unique()
)

selected_skills = st.multiselect(
    "Skills",
    sorted(all_skills)
)

# =========================
# SEMANTIC SEARCH LOGIC
# =========================
filtered = jobs.copy()

if search_button and semantic_query:

    st.info(f"Searching for: {semantic_query}")

    # 1. Create embedding
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=semantic_query
    ).data[0].embedding

    # 2. Vector search in PostgreSQL (pgvector required)
    results = pd.read_sql(
        """
        SELECT job_id, job_title, employer_name, job_city, job_state,
               experience_level, role_category, skills, job_description
        FROM jobs_ca_new
        ORDER BY embedding <-> %s
        LIMIT 20;
        """,
        engine,
        params=[query_embedding]
    )

    filtered = results

# =========================
# APPLY TRADITIONAL FILTERS (AFTER SEMANTIC SEARCH)
# =========================

if role_filter != "All":
    filtered = filtered[filtered["role_category"] == role_filter]

if province_filter != "All":
    filtered = filtered[filtered["job_state"] == province_filter]

if experience_filter != "All":
    filtered = filtered[filtered["experience_level"] == experience_filter]

if remote_filter == "Remote":
    filtered = filtered[filtered["job_is_remote"] == 1]

if remote_filter == "On-Site":
    filtered = filtered[filtered["job_is_remote"] == 0]

if keyword:
    filtered = filtered[
        filtered["job_title"].str.contains(keyword, case=False, na=False)
    ]

if selected_skills:
    for skill in selected_skills:
        filtered = filtered[
            filtered["skills"].str.contains(skill, case=False, na=False)
        ]

# =========================
# RESULTS
# =========================
st.metric("Matching Jobs", len(filtered))

st.subheader("Job Results")

for _, row in filtered.iterrows():
    with st.container():
        st.markdown(f"""
        ### 💼 {row['job_title']}
        **🏢 {row['employer_name']}**  
        📍 {row['job_city']}, {row['job_state']}  
        🎯 {row['experience_level']} | {row['role_category']}  
        🧠 Skills: {row['skills']}

        ---
        """)