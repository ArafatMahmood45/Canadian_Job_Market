import streamlit as st
import pandas as pd
from openai import OpenAI

from src.config import OPENAI_API_KEY
from src.database import engine
from src.job_features import normalize_locations


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Search Jobs",
    layout="wide"
)

st.title("🇨🇦 AI Job Search - Canada")


# =========================
# OPENAI CLIENT
# =========================

client = OpenAI(
    api_key=OPENAI_API_KEY
)


# =========================
# SESSION STATE
# =========================

if "search_results" not in st.session_state:
    st.session_state.search_results = None


# =========================
# AI SEARCH SECTION
# =========================

st.subheader("🤖 AI Semantic Job Search")


st.info(
    """
    Describe the job you are looking for.

    Examples:

    • Entry-level Data Engineering jobs in Toronto
    • AI engineering roles requiring python, R, C++ skills
    • Machine learning co-op opportunities for students and recent graduates
    """
)


semantic_query = st.text_area(
    "What type of job are you looking for?",
    placeholder="Example: I am looking for a data engineer role in Toronto, I have experience with python, SQL, fabric, data pipelines"
)


search_button = st.button(
    "🔍 Search Jobs"
)


# =========================
# SEMANTIC SEARCH
# =========================

if search_button and semantic_query:


    st.info(
        f"Searching for: {semantic_query}"
    )


    # Create query embedding

    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=semantic_query
    ).data[0].embedding


    # Convert embedding to pgvector format

    query_vector = (
        "["
        + ",".join(map(str, query_embedding))
        + "]"
    )


    # Vector similarity search

    results = pd.read_sql(
        """
        SELECT
            job_id,
            job_title,
            employer_name,
            job_city,
            job_state,
            job_country,
            job_is_remote,
            experience_level,
            role_category,
            skills,
            job_description

        FROM jobs_new_ca

        ORDER BY embedding <-> CAST(%s AS vector)

        LIMIT 50;
        """,
        engine,
        params=(query_vector,)
    )
    results = normalize_locations(results)


    results["skills"] = results["skills"].fillna(
        "Unknown"
    )


    # Store results

    st.session_state.search_results = results



# =========================
# DISPLAY FILTERS
# ONLY AFTER SEARCH
# =========================

if st.session_state.search_results is not None:


    filtered = st.session_state.search_results.copy()


    st.divider()

    st.subheader(
        "Refine Search Results"
    )


    # -------------------------
    # FILTERS
    # -------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        role_filter = st.selectbox(
            "Role Category",
            [
                "All"
            ]
            +
            sorted(
                filtered["role_category"]
                .dropna()
                .unique()
            )
        )


    with col2:

        province_filter = st.selectbox(
            "Province",
            [
                "All"
            ]
            +
            sorted(
                filtered["job_state"]
                .dropna()
                .unique()
            )
        )


    with col3:

        experience_filter = st.selectbox(
            "Experience Level",
            [
                "All"
            ]
            +
            sorted(
                filtered["experience_level"]
                .dropna()
                .unique()
            )
        )



    col4, col5 = st.columns(2)


    with col4:

        remote_filter = st.selectbox(
            "Work Type",
            [
                "All",
                "Remote",
                "On-Site"
            ]
        )


    with col5:

        keyword = st.text_input(
            "Search Job Title"
        )



    # -------------------------
    # SKILL FILTER
    # -------------------------

    all_skills = (
        filtered["skills"]
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
    # APPLY FILTERS
    # =========================


    if role_filter != "All":

        filtered = filtered[
            filtered["role_category"]
            == role_filter
        ]


    if province_filter != "All":

        filtered = filtered[
            filtered["job_state"]
            == province_filter
        ]


    if experience_filter != "All":

        filtered = filtered[
            filtered["experience_level"]
            == experience_filter
        ]


    if remote_filter == "Remote":

        filtered = filtered[
            filtered["job_is_remote"] == 1
        ]


    if remote_filter == "On-Site":

        filtered = filtered[
            filtered["job_is_remote"] == 0
        ]


    if keyword:

        filtered = filtered[
            filtered["job_title"]
            .str.contains(
                keyword,
                case=False,
                na=False
            )
        ]



    if selected_skills:

        for skill in selected_skills:

            filtered = filtered[
                filtered["skills"]
                .str.contains(
                    skill,
                    case=False,
                    na=False
                )
            ]



    # =========================
    # RESULTS
    # =========================

    st.divider()


    st.metric(
        "Matching Jobs",
        len(filtered)
    )


    st.subheader(
        "Recommended Jobs"
    )



    if len(filtered) == 0:

        st.warning(
            "No jobs match your filters."
        )


    else:

        for _, row in filtered.iterrows():

            with st.container():

                st.markdown(
                    f"""
                    ### 💼 {row['job_title']}

                       Company: {row['employer_name']}

                       Location: {row['job_city']}, {row['job_state']}

                       Level: {row['experience_level']} | Category: {row['role_category']}

                       Skills: {row['skills']}

                    ---
                    """
                )

else:

    st.info(
        "Enter a job description above to begin searching."
    )