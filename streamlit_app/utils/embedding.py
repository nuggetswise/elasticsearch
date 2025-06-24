import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st

# Use a cached model for efficiency
@st.cache_resource
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def embed_chunks(chunks):
    model = get_model()
    return model.encode(chunks, show_progress_bar=False)

@st.cache_data
def embed_query(query):
    model = get_model()
    return model.encode([query])[0]

@st.cache_data
def get_top_chunks(query, chunks, top_k=3):
    chunk_embeddings = embed_chunks(chunks)
    query_embedding = embed_query(query)
    similarities = np.dot(chunk_embeddings, query_embedding) / (
        np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-8)
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]
