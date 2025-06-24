import streamlit as st

def query_input():
    with st.form(key="query_form"):
        query = st.text_input("Enter your search query:")
        st.markdown(
            "> **Note:** This app will show a side-by-side comparison of Lexical (BM25), Semantic (Embeddings), Hybrid, and LLM-based search results for your query."
        )
        submitted = st.form_submit_button("Run Search")
    if submitted:
        return query
    return None
