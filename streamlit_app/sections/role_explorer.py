import streamlit as st
from utils.llm import summarize_job_post

# Path to the job post markdown
JOB_POST_PATH = "data/elastic_job_post.md"

@st.cache_data
def load_job_post():
    with open(JOB_POST_PATH, "r") as f:
        return f.read()

def render():
    st.header("🧭 Role Explorer")
    st.markdown("#### Elastic Senior Product Manager, Search — Role Breakdown")
    job_post = load_job_post()
    summary = summarize_job_post(job_post)
    col1, col2 = st.columns([2, 3])
    with col1:
        st.subheader("Summary")
        st.markdown("**Responsibilities:**\n" + summary["responsibilities"])
        st.markdown("**Key Product Areas:**\n" + summary["product_areas"])
        st.markdown("**Skills & Requirements:**\n" + summary["skills"])
        if summary.get("metrics"):
            st.markdown("**Metrics / KPIs:**\n" + summary["metrics"])
    with col2:
        st.markdown("##### Full Job Description")
        st.code(job_post, language="markdown")
