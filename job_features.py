import ast

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

# df["experience_level"] = df.apply(
#     lambda row: get_experience_level(row.get("job_title", ""),
#                                      row.get("job_description", "")), axis=1
# )

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

def get_role_categories(title, description):
    text = f'{title} {description}'.lower()

    for category, keywords in role_categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "unknown"


def get_city(location):
    area = location.get("area", [])

    if len(area) >= 3:
        return area[-1]

    return "Unknown"


def get_state(location):
    area = location.get("area", [])

    if len(area) >= 2:
        return area[-2]

    return "Unknown"


def safe_parse(x):
    if isinstance(x, dict):
        return x
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except:
            return {}
    return {}

