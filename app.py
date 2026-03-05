import streamlit as st
import pandas as pd

from github_api import check_repo_exists
from sonar_api import check_project_exists, get_issues
from utils import extract_repo_details, create_project_key


st.set_page_config(page_title="GitHub Repo Analyzer")

st.title("🔍 GitHub Repository Code Quality Analyzer")

repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/user/repo"
)

analyze = st.button("Analyze Repository")


if analyze:

    if repo_url == "":
        st.warning("Please enter a repository URL")
        st.stop()

    owner, repo = extract_repo_details(repo_url)

    st.info("Checking repository...")

    repo_exists = check_repo_exists(owner, repo)

    if not repo_exists:

        st.error("Repository not found or private.")
        st.stop()

    st.success("Repository is valid and public")

    project_key = create_project_key(owner, repo)

    st.info("Checking SonarCloud onboarding...")

    onboarded = check_project_exists(project_key)

    if not onboarded:

        st.warning("This repository is not onboarded in SonarCloud.")

        st.markdown("""
### How to onboard the repository

1. Login to SonarCloud
2. Click **Analyze New Project**
3. Select this repository
4. Complete setup
5. Return here and click Analyze again
""")

        st.stop()

    st.info("Fetching analysis report...")

    issues = get_issues(project_key)

    if len(issues) == 0:
        st.success("No issues found 🎉")
        st.stop()

    data = []

    for issue in issues:

        data.append({
            "Type": issue["type"],
            "Severity": issue["severity"],
            "Message": issue["message"],
            "Component": issue["component"]
        })

    df = pd.DataFrame(data)

    st.subheader("Analysis Report")

    st.dataframe(df)

    bugs = df[df["Type"] == "BUG"].shape[0]
    vulnerabilities = df[df["Type"] == "VULNERABILITY"].shape[0]
    smells = df[df["Type"] == "CODE_SMELL"].shape[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Bugs", bugs)
    col2.metric("Vulnerabilities", vulnerabilities)
    col3.metric("Code Smells", smells)