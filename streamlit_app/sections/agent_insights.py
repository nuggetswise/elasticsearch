import streamlit as st
from utils.llm import agent_insight_response
from utils.chunking import chunk_job_post

JOB_POST_PATH = "data/elastic_job_post.md"

@st.cache_data
def load_job_post():
    with open(JOB_POST_PATH, "r") as f:
        return f.read()

@st.cache_data
def get_chunks():
    return chunk_job_post(load_job_post())

def render():
    st.header("🧠 Agent Insights")
    st.markdown("Simulate Nuggetwise-style agent logic for interview prep and strategy.")
    prompt = st.text_area("Enter a custom prompt (e.g. 30-60-90 day plan, roadmap ideas):")
    if prompt:
        job_chunks = get_chunks()
        response = agent_insight_response(prompt, job_chunks)
        st.markdown("**Agent Response:**")
        st.success(response)
