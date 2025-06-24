import streamlit as st
from components.query_input import query_input
from components.results_display import results_display
from components.explain_toggle import explain_toggle
import json
from utils.dummy_docs import DOCS

st.set_page_config(page_title="Smart Query Lab", layout="centered")
st.title("🧪 Smart Query Lab: Search Mode Comparison")

# --- Sidebar: Only show upload and hybrid weight (no tags/types) ---
st.sidebar.header("Customization")
user_docs = None
uploaded = st.sidebar.file_uploader("Upload JSON doc set (<1MB)", type=["json"])
if uploaded:
    try:
        user_docs = json.load(uploaded)
        assert isinstance(user_docs, list)
        st.sidebar.success(f"Loaded {len(user_docs)} docs from upload.")
    except Exception as e:
        st.sidebar.error(f"Invalid JSON: {e}")
        user_docs = None
all_docs = user_docs if user_docs is not None else DOCS
hybrid_weight = st.sidebar.slider("Hybrid Semantic Weight", 0.0, 1.0, 0.6, 0.05)

# --- Attach sample data on sidebar with description and download ---
st.sidebar.markdown('---')
st.sidebar.markdown('**Sample Data**')
sample_desc = "This sample data contains 5 documents about search, including Elasticsearch tuning, BM25, vector search, hybrid patterns, and scaling systems. Each document has a title, author, date, snippet, tags, and type."
st.sidebar.caption(sample_desc)
st.sidebar.download_button(
    label="Download Sample Data (JSON)",
    data=json.dumps(DOCS, indent=2),
    file_name="sample_data.json",
    mime="application/json"
)

# --- Sample search queries ---
st.sidebar.markdown('---')
st.sidebar.markdown('**Sample Search Queries**')
sample_queries = [
    "elasticsearch performance",
    "bm25 ranking",
    "semantic vector search",
    "hybrid retrieval",
    "scaling search systems"
]
for q in sample_queries:
    st.sidebar.code(q)

# --- Main UI ---
query = query_input()
explain = explain_toggle()

if query:
    from utils.llm import explain_retrieval_strategy_stream
    with st.spinner("Retrieving and ranking documents..."):
        results_display(query, filters=None, hybrid_weight=hybrid_weight, user_docs=user_docs)
    if explain:
        st.markdown("---")
        st.markdown("**How LLM is used (streaming):**")
        for chunk in explain_retrieval_strategy_stream("Comparison"):
            st.write(chunk)
