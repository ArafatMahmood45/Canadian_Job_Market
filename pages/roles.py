import streamlit as st
import pandas as pd
from src.database import engine
from src.job_features import normalize_locations

st.set_page_config(
    page_title="Roles Analysis",
    layout="wide"
)

st.title("Roles Analysis")

# Load data

engine = engine

jobs = pd.read_sql(
    "SELECT * FROM jobs_new_ca",
    engine
)

jobs = jobs.copy()
jobs = normalize_locations(jobs)

# Remove unknown roles
jobs = jobs[jobs["role_category"] != "unknown"]

# ==========================
# KPIs
# ==========================

most_common_role = (
    jobs["role_category"]
    .value_counts()
    .idxmax()
)

total_roles = (
    jobs["role_category"]
    .nunique()
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Most Common Role",
        most_common_role
    )

with col2:
    st.metric(
        "Role Categories",
        total_roles
    )

# ==========================
# Jobs by Role Category
# ==========================

st.subheader("Jobs by Role Category")

role_counts = (
    jobs["role_category"]
    .value_counts()
)

st.bar_chart(role_counts)

# ==========================
# Experience Level by Role
# ==========================

st.subheader("Experience Level by Role")

experience_role = (
    jobs.groupby(
        ["role_category", "experience_level"]
    )
    .size()
    .unstack(fill_value=0)
)

st.bar_chart(experience_role)

# ==========================
# Role Explorer
# ==========================

st.subheader("Role Explorer")

selected_role = st.selectbox(
    "Select Role Category",
    sorted(jobs[jobs["role_category"] != "unknown"]["role_category"].unique())
)

filtered = jobs[
    jobs["role_category"] == selected_role
]

# ==========================
# Top Employers
# ==========================

st.subheader(
    f"Top Employers for {selected_role}"
)

top_employers = (
    filtered["employer_name"]
    .value_counts()
    .head(10)
)

st.bar_chart(top_employers)

# ==========================
# Top Provinces
# ==========================

st.subheader(
    f"Top Provinces for {selected_role}"
)

province_counts = (
    filtered[
        filtered["job_state"] != "unknown"
    ]["job_state"]
    .value_counts()
    .head(10)
)

st.bar_chart(province_counts)

# ==========================
# Top Cities
# ==========================

st.subheader(
    f"Top Cities for {selected_role}"
)

city_counts = (
    filtered[
        filtered["job_city"] != "unknown"
    ]["job_city"]
    .value_counts()
    .head(10)
)

st.bar_chart(city_counts)

# ==========================
# Jobs Table
# ==========================

st.subheader(
    f"Sample {selected_role} Jobs"
)

st.dataframe(
    filtered[
        [
            "job_title",
            "employer_name",
            "job_city",
            "job_state",
            "experience_level"
        ]
    ]
)