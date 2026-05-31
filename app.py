import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Canadian Job Market Intelligence")

st.title("(CA) Canadian Job Market Intelligence")

connection = sqlite3.connect("data.db")
jobs = pd.read_sql("SELECT * FROM jobs_ca", connection)


st.metric("Total Jobs:", len(jobs))

st.dataframe(jobs)