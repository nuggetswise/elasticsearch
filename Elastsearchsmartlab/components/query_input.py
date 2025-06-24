import streamlit as st

def query_input():
    with st.form(key="query_form"):
        query = st.text_area(
            "Enter your search query:",
            height=80  # About 2x the default height
        )
        st.markdown(
            "> **Note:** This app will show a side-by-side comparison of Lexical (BM25), Semantic (Embeddings), Hybrid, and LLM-based search results for your query."
        )
        st.markdown('**Sample Search Queries:**')
        sample_queries = [
            "elasticsearch performance",
            "bm25 ranking",
            "semantic vector search",
            "hybrid retrieval",
            "scaling search systems"
        ]
        for q in sample_queries:
            st.code(q)
        submitted = st.form_submit_button("Run Search")
    if submitted:
        return query
    return None
