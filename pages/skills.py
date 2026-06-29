import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Skills Analysis", layout="wide")

st.title("Skills Analysis (Canada Job Market)")

# Load data
connection = sqlite3.connect("data.db")
jobs = pd.read_sql("SELECT * FROM jobs_ca", connection)

jobs = jobs.copy()

# Ensure skills are usable (they are stored as comma-separated strings)
jobs["skills"] = jobs["skills"].fillna("unknown")

# -----------------------------
# KPIs
# -----------------------------
st.subheader("Key Insights")
# remember to remove col4
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_unique_skills = (
        jobs["skills"]
        .str.split(", ")
        .explode()
        .nunique()
    )
    st.metric("Unique Skills", total_unique_skills)

with col2:
    most_common_skill = (
        jobs["skills"]
        .str.split(", ")
        .explode()
        .value_counts()
        .idxmax()
    )
    st.metric("Most In-Demand Skill", most_common_skill)

with col3:
    avg_skills_per_job = jobs["skills_count"].mean()
    st.metric("Avg Skills per Job", round(avg_skills_per_job, 2))

with col4:
    med_skills_per_job = jobs["skills_count"].median()
    st.metric("Avg Skills per Job", round(avg_skills_per_job, 2))

# -----------------------------
# Top Skills Chart
# -----------------------------
st.subheader("Top 20 Skills in Canada")

skills_series = (
    jobs["skills"]
    .str.split(", ")
    .explode()
)

top_skills = (
    skills_series
    .value_counts()
    .head(20)
)

st.bar_chart(top_skills)

# -----------------------------
# Skills by Role Category
# -----------------------------
st.subheader("Skills by Role Category")

role_selected = st.selectbox(
    "Select Role Category",
    jobs["role_category"].unique()
)

filtered = jobs[jobs["role_category"] == role_selected]

role_skills = (
    filtered["skills"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(15)
)

st.bar_chart(role_skills)

# -----------------------------
# Skill frequency table (optional)
# -----------------------------
st.subheader("Skill Breakdown Table")

skill_table = (
    skills_series
    .value_counts()
    .reset_index()
)

skill_table.columns = ["Skill", "Count"]

st.dataframe(skill_table)

# this too
st.title("Skills Analysis (Canada Job Market)")

st.caption(
    "Explore the most in-demand technical skills across AI, Data, Cloud, and Software Engineering roles in Canada."
)