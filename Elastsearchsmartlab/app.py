import streamlit as st
from components.query_input import query_input
from components.results_display import results_display
from components.explain_toggle import explain_toggle
import json
from utils.dummy_docs import DOCS

st.set_page_config(page_title="Smart Query Lab", layout="centered")

# --- Header with clear description ---
st.title("🧪 Smart Query Lab: Search Mode Comparison")
st.markdown("""
**Compare different search strategies in real-time!** This tool helps you understand how lexical (keyword-based), 
semantic (meaning-based), and hybrid search approaches perform on your queries.
""")

# --- Quick Start Guide ---
with st.expander("🚀 Quick Start Guide", expanded=True):
    st.markdown("""
    1. **Enter a search query** in the box below
    2. **Adjust the Hybrid Weight** slider to balance keyword vs semantic search
    3. **Upload your own data** (optional) or use the sample data
    4. **Toggle 'Explain'** to get AI-powered insights about search strategies
    5. **Compare results** across different search modes
    """)

# --- Sidebar with better organization ---
st.sidebar.header("⚙️ Configuration")

# Hybrid Weight with better explanation
st.sidebar.markdown("**🔧 Search Strategy Balance**")
st.sidebar.markdown("""
- **0.0** = Pure keyword search (BM25)
- **0.5** = Balanced hybrid approach  
- **1.0** = Pure semantic search (vectors)
""")
hybrid_weight = st.sidebar.slider(
    "Hybrid Semantic Weight", 
    0.0, 1.0, 0.6, 0.05,
    help="Balance between keyword matching and semantic understanding"
)

# Document upload with better instructions
st.sidebar.markdown("---")
st.sidebar.markdown("**📁 Your Data (Optional)**")
st.sidebar.markdown("Upload your own documents to test search on your content:")
uploaded = st.sidebar.file_uploader(
    "Upload JSON document set (<1MB)", 
    type=["json"],
    help="Upload a JSON file with an array of document objects. Each document should have: title, snippet, date, author, tags, type"
)

if uploaded:
    try:
        user_docs = json.load(uploaded)
        assert isinstance(user_docs, list)
        st.sidebar.success(f"✅ Loaded {len(user_docs)} documents successfully!")
    except Exception as e:
        st.sidebar.error(f"❌ Invalid JSON format: {e}")
        user_docs = None
else:
    st.sidebar.info("💡 No file uploaded - using sample data")

all_docs = user_docs if user_docs is not None else DOCS

# Sample data section with better description
st.sidebar.markdown("---")
st.sidebar.markdown("**📚 Sample Data**")
st.sidebar.markdown("""
This sample contains 5 documents about search technologies:
- Elasticsearch tuning & performance
- BM25 ranking algorithms  
- Vector search & embeddings
- Hybrid search patterns
- System scaling strategies
""")
st.sidebar.download_button(
    label="📥 Download Sample Data (JSON)",
    data=json.dumps(DOCS, indent=2),
    file_name="sample_data.json",
    mime="application/json",
    help="Download the sample data to see the expected JSON format"
)

# Sample queries with better presentation
st.sidebar.markdown("---")
st.sidebar.markdown("**🔍 Try These Queries**")
st.sidebar.markdown("Click any query below to test it:")
sample_queries = [
    "elasticsearch performance",
    "bm25 ranking", 
    "semantic vector search",
    "hybrid retrieval",
    "scaling search systems"
]

# Make queries clickable
for i, q in enumerate(sample_queries):
    if st.sidebar.button(f"🔍 {q}", key=f"query_{i}"):
        st.session_state.sample_query = q

# --- Main UI with better instructions ---
st.markdown("---")
st.markdown("### 🔎 Enter Your Search Query")
st.markdown("Type a query to see how different search strategies rank the results:")

# Get query input
query = query_input()

# Add sample query if selected
if hasattr(st.session_state, 'sample_query'):
    query = st.session_state.sample_query
    del st.session_state.sample_query

# Explain toggle with better description
st.markdown("---")
explain = explain_toggle()
if explain:
    st.info("🤖 **AI Explanation Enabled**: You'll see an AI-powered explanation of how the search strategies work after running a query.")

# --- Results Section ---
if query:
    st.markdown("---")
    st.markdown(f"### 📊 Search Results for: **'{query}'**")
    
    from utils.llm import explain_retrieval_strategy_stream
    with st.spinner("🔍 Searching and ranking documents..."):
        results_display(query, filters=None, hybrid_weight=hybrid_weight, user_docs=user_docs)
    
    if explain:
        st.markdown("---")
        st.markdown("### 🤖 AI Explanation: How Search Strategies Work")
        st.markdown("Here's how the different search approaches work:")
        
        # Fix: Buffer the LLM output for proper formatting
        explanation_text = ""
        explanation_placeholder = st.empty()
        
        for chunk in explain_retrieval_strategy_stream("Comparison"):
            explanation_text += chunk
            # Update the placeholder with the accumulated text
            explanation_placeholder.markdown(explanation_text)
else:
    # Show helpful message when no query
    st.markdown("---")
    st.info("💡 **Ready to search!** Enter a query above or click one of the sample queries in the sidebar to get started.")

# --- Footer with additional info ---
st.markdown("---")
st.markdown("""
---
**🧪 Smart Query Lab** - Built for exploring search technologies and comparing retrieval strategies.
""")
