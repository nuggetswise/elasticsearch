import streamlit as st

def query_input():
    with st.form(key="query_form"):
        # Better query input with placeholder and help text
        query = st.text_area(
            "Enter your search query:",
            height=80,
            placeholder="e.g., 'elasticsearch performance' or 'how does BM25 work?'",
            help="Type your search query here. You can ask questions or use keywords."
        )
        
        # Clear explanation of what will happen
        st.markdown("""
        **🔍 What happens when you search:**
        - **Lexical Search (BM25)**: Finds documents with exact keyword matches
        - **Semantic Search**: Finds documents with similar meaning using AI embeddings  
        - **Hybrid Search**: Combines both approaches for better results
        - **LLM Scoring**: Uses AI to rate document relevance
        """)
        
        # Better sample queries section
        st.markdown("**💡 Try these example queries:**")
        sample_queries = [
            "elasticsearch performance",
            "bm25 ranking",
            "semantic vector search", 
            "hybrid retrieval",
            "scaling search systems"
        ]
        
        # Display sample queries in a more compact way
        cols = st.columns(len(sample_queries))
        for i, q in enumerate(sample_queries):
            with cols[i]:
                st.markdown(f"`{q}`")
        
        # Submit button with better styling
        submitted = st.form_submit_button(
            "🚀 Run Search & Compare Results",
            help="Click to see how different search strategies rank your results"
        )
        
    if submitted and query.strip():
        return query.strip()
    return None
