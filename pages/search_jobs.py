import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Search Jobs",
    layout="wide"
)

st.title("Search Jobs (Canada Job Market)")

st.subheader("AI Job Search")

st.info(
    """
    🤖 **AI Semantic Jobs Search**

    Describe the kind of job you're looking for in natural language.

    Examples:
    - Entry-level AI jobs in Toronto
    - Remote Python developer jobs with SQL
    - Machine learning roles suitable for new graduates
    - Data engineering jobs requiring Spark and AWS
    """
)

semantic_query = st.text_area(
    "Describe the job you're looking for",
    placeholder="Example: Looking for entry-level AI job in Toronto that require Python and machine learning skills"
)

semantic_search = st.button("Search with AI")

if semantic_search and semantic_query:
    st.info(f"Searching for: {semantic_query}")

# =========================
# Load Data
# =========================
connection = sqlite3.connect("data.db")

jobs = pd.read_sql(
    "SELECT * FROM jobs_ca",
    connection
)

jobs = jobs.copy()

# Clean missing values
jobs["skills"] = jobs["skills"].fillna("unknown")

# =========================
# Sidebar Filters
# =========================

st.subheader("Filters")

col1, col2, col3 = st.columns(3)

# -------------------------
# Role Filter
# -------------------------
with col1:
    role_filter = st.selectbox(
        "Role Category",
        ["All"] + sorted(jobs["role_category"].unique())
    )

# -------------------------
# Province Filter
# -------------------------
with col2:
    province_filter = st.selectbox(
        "Province",
        ["All"] + sorted(jobs["job_state"].unique())
    )

# -------------------------
# Experience Filter
# -------------------------
with col3:
    experience_filter = st.selectbox(
        "Experience Level",
        ["All"] + sorted(jobs["experience_level"].unique())
    )

# =========================
# Second Row Filters
# =========================

col4, col5 = st.columns(2)

# -------------------------
# Remote Filter
# -------------------------
with col4:
    remote_filter = st.selectbox(
        "Work Type",
        ["All", "Remote", "On-Site"]
    )

# -------------------------
# Keyword Search
# -------------------------
with col5:
    keyword = st.text_input(
        "Search Job Title"
    )

# =========================
# Skills Multi-Select
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
# Filtering Logic
# =========================

filtered = jobs.copy()

# Role filter
if role_filter != "All":
    filtered = filtered[
        filtered["role_category"] == role_filter
    ]

# Province filter
if province_filter != "All":
    filtered = filtered[
        filtered["job_state"] == province_filter
    ]

# Experience filter
if experience_filter != "All":
    filtered = filtered[
        filtered["experience_level"] == experience_filter
    ]

# Remote filter
if remote_filter == "Remote":
    filtered = filtered[filtered["job_is_remote"] == 1]

if remote_filter == "On-Site":
    filtered = filtered[filtered["job_is_remote"] == 0]

# Keyword search
if keyword:
    filtered = filtered[
        filtered["job_title"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

# Skills filter (MULTI-SELECT)
if selected_skills:
    for skill in selected_skills:
        filtered = filtered[
            filtered["skills"].str.contains(
                skill,
                case=False,
                na=False
            )
        ]

# =========================
# Results Summary
# =========================

st.metric(
    "Matching Jobs",
    len(filtered)
)

# =========================
# Results Table
# =========================

st.subheader("Job Results")

st.dataframe(
    filtered[
        [
            "job_title",
            "employer_name",
            "job_city",
            "job_state",
            "experience_level",
            "role_category",
            "skills"
        ]
    ],
    use_container_width=True
)