import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Canadian Job Market Intelligence", layout="wide")

st.title("(CA) Canadian Job Market Intelligence")

connection = sqlite3.connect("data.db")

jobs = pd.read_sql("SELECT * FROM jobs_ca", connection)
jobs = jobs.copy()


# KPIs


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs:", len(jobs))

with col2:
    st.metric("Cities:", jobs.job_city.nunique())

with col3:
    st.metric("Employers:", jobs.employer_name.nunique())

with col4:
    jobs["job_posted_at_datetime_utc"] = pd.to_datetime(
        jobs["job_posted_at_datetime_utc"],
        errors="coerce"
    )
    latest_job = jobs["job_posted_at_datetime_utc"].max()
    st.metric("Latest Job Posted:", latest_job.strftime("%d %B %Y"))

#  Province Chart
st.subheader("Jobs by Province")

province_counts = (
    jobs[jobs["job_state"] != 'Unknown']["job_state"]
    .value_counts()
    .rename_axis("Province")
    .reset_index(name="Jobs")
)

st.bar_chart(province_counts.set_index("Province"))

#  Cities Chart
st.subheader("Top Cities")

city_counts = (
    jobs[jobs["job_city"] != "Unknown"]["job_city"]
    .value_counts()
    .head(10)
)

st.bar_chart(city_counts)

#  Role Categories Chart
st.subheader("Role Categories")

role_counts = jobs[jobs["role_category"] != "Unknown"]["role_category"].value_counts()

st.bar_chart(role_counts)

#  Job Posted by month
jobs["day"] = jobs["job_posted_at_datetime_utc"].dt.date

daily_jobs = jobs.groupby("day").size().sort_index()


st.subheader("Jobs Posted by Day")
st.line_chart(daily_jobs)
