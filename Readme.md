# 🇨🇦 Canadian Job Market Intelligence Platform

A data engineering and analytics platform that collects Canadian technology job postings, transforms raw job market data, stores it in a database, and presents insights through an interactive dashboard.

## Project Goal

The objective of this project is to help job seekers understand hiring trends across Canada by providing data-driven insights into:

- Job availability
- Geographic demand
- Role distribution
- Hiring activity over time
- Required skills and qualifications

---

## What I Built

### Automated ETL Pipeline

Designed and implemented an end-to-end ETL pipeline that:

- Extracts job postings from an external API
- Handles API rate limits and retries
- Cleans and validates raw data
- Removes duplicate job postings
- Performs feature engineering
- Loads processed data into SQLite

### Data Modeling

Created a structured job database containing:

- Job information
- Location data
- Employer information
- Experience-level classifications
- Role categories
- Skill-related features

### Feature Engineering

Developed custom functions to:

- Classify experience levels
- Categorize job roles
- Extract and count technical skills from job descriptions

### Interactive Analytics Dashboard

Built a Streamlit dashboard that provides:

- Market overview KPIs
- Hiring activity by province
- Top hiring cities
- Role distribution analysis
- Job posting trends over time

---

## Technologies Used

- Python
- Pandas
- SQLite
- Streamlit
- Requests
- Python Dotenv
- Schedule

---

## Skills Demonstrated

### Data Engineering

- ETL Pipeline Development
- Data Cleaning and Transformation
- API Integration
- Database Design
- SQLite

### Data Analysis

- Exploratory Data Analysis
- Feature Engineering
- Data Aggregation
- Trend Analysis

### Software Engineering

- Object-Oriented Programming
- Modular Code Organization
- Error Handling
- Automation and Scheduling

### Data Visualization

- Interactive Dashboards
- KPI Reporting
- Business Intelligence Concepts
- Streamlit Development

---

## Current Features

- Automated job collection
- Daily ETL execution
- SQLite data storage
- Market overview dashboard
- Province-level analysis
- City-level analysis
- Hiring trend analysis
- Embedding

---

## Planned Enhancements

- Skills Intelligence Dashboard
- Job Search Interface
- Advanced Role Analytics
- AI-Powered Market Insights
- Agentic AI Career Assistant
- Retrieval-Augmented Generation (RAG)

---

## Project Structure

```text
Canadian_Job_Platform/
│
├── app.py
├── etl.py
├── run.py
├── job_features.py
├── data.db
└── README.md
```

## Status

🚧 Active Development

The ETL pipeline and Market Overview dashboard are currently operational, with additional analytics and AI-powered features in development.