import streamlit as st
import PyPDF2
import numpy as np

from utils.embedding import get_top_chunks, embed_query, embed_chunks
from utils.llm import simulate_llm_response
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
    st.header("🔍 Nuggetwise Simulator")
    st.markdown("Simulate how Nuggetwise grounds answers in job post context.")
    question = st.text_input("Ask a question about the Elastic role:")
    if question:
        chunks = get_chunks()
        top_chunks = get_top_chunks(question, chunks)
        st.markdown("**Top-3 Retrieved Chunks:**")
        for i, chunk in enumerate(top_chunks, 1):
            st.info(f"Chunk {i}:\n{chunk}")
        llm_response = simulate_llm_response(question, top_chunks)
        st.markdown("---")
        st.markdown("**Nuggetwise-style LLM Response:**")
        st.success(llm_response)

    st.markdown("---")
    st.subheader("📄 Resume-to-Role Matching (Bonus)")
    uploaded_file = st.file_uploader("Upload your PDF resume to see top-matching job post nuggets:", type=["pdf"])
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = "\n".join(page.extract_text() or '' for page in reader.pages)
            if not resume_text.strip():
                st.warning("No text could be extracted from the PDF.")
                return
            chunks = get_chunks()
            resume_embedding = embed_query(resume_text)
            chunk_embeddings = embed_chunks(chunks)
            similarities = np.dot(chunk_embeddings, resume_embedding) / (
                np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(resume_embedding) + 1e-8)
            top_indices = np.argsort(similarities)[-3:][::-1]
            st.markdown("**Top-3 Job Post Chunks Matching Your Resume:**")
            for i in top_indices:
                st.info(f"Chunk {i+1}:\n{chunks[i]}")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
