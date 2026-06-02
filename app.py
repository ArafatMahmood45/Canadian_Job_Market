import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Canadian Job Market Intelligence", layout="wide")

st.title("(CA) Canadian Job Market Intelligence")

connection = sqlite3.connect("data.db")
jobs = pd.read_sql("SELECT * FROM jobs_ca", connection)

# KPIs

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs:", len(jobs))

with col2:
    st.metric("Cities:", jobs.job_city.nunique())

with col3:
    st.metric("Employers:", jobs.employer_name.nunique())

with col4:
    st.metric("Remote:", jobs.job_is_remote.sum())

#  Province Chart
st.subheader("Jobs by Province")

province_counts = (
    jobs["job_state"]
    .value_counts()
    .reset_index()
)

province_counts.columns = ["Province", "Jobs"]

st.bar_chart(
    province_counts.set_index("Province")
)

#  Cities Chart
st.subheader("Top Cities")

city_counts = (
    jobs["job_city"]
    .value_counts()
    .head(10)
)

st.bar_chart(city_counts)

#  Role Categories Chart
st.subheader("Role Categories")

role_counts = jobs["role_category"].value_counts()

st.bar_chart(role_counts)

#  Experience level Chart
st.subheader("Experience Levels")

experience_counts = jobs["experience_level"].value_counts()

st.bar_chart(experience_counts)