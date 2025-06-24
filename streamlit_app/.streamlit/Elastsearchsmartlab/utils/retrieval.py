import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st
from utils.dummy_docs import DOCS
from rank_bm25 import BM25Okapi

@st.cache_resource
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def embed_texts(texts):
    model = get_model()
    return model.encode(texts, show_progress_bar=False)

def filter_docs(docs, filters):
    return docs  # Filtering logic can be added if needed

def get_bm25_scores(query, docs):
    tokenized_corpus = [doc['snippet'].lower().split() for doc in docs]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    return scores

def get_semantic_scores(query, docs):
    titles = [doc["title"] for doc in docs]
    doc_embs = embed_texts(titles)
    q_emb = embed_texts([query])[0]
    scores = np.dot(doc_embs, q_emb) / (np.linalg.norm(doc_embs, axis=1) * np.linalg.norm(q_emb) + 1e-8)
    return scores

def get_llm_scores(query, docs):
    import openai
    api_key = st.secrets.get("openai_api_key", None)
    if not api_key:
        # If no API key, return zeros for all docs and skip LLM scoring
        return np.zeros(len(docs))
    openai.api_key = api_key
    scores = []
    for doc in docs:
        prompt = f"Given the query: '{query}', rate the relevance of the following document (0-1):\nTitle: {doc['title']}\nSnippet: {doc['snippet']}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.0,
            )
            text = response["choices"][0]["message"]["content"].strip()
            score = float(text.split()[0]) if text.split() else 0.0
        except Exception:
            score = 0.0
        scores.append(score)
    return np.array(scores)

def get_simulated_results(query, mode, filters=None, hybrid_weight=0.6, user_docs=None):
    docs = user_docs if user_docs is not None else DOCS
    docs = filter_docs(docs, filters)
    if not docs:
        return []
    if mode == "Lexical":
        scores = get_bm25_scores(query, docs)
        method = "BM25"
    elif mode == "Semantic":
        scores = get_semantic_scores(query, docs)
        method = "Sentence-Transformers Embedding"
    elif mode == "LLM":
        scores = get_llm_scores(query, docs)
        method = "LLM (GPT-4)"
    else:  # Hybrid
        sem_scores = get_semantic_scores(query, docs)
        lex_scores = get_bm25_scores(query, docs)
        scores = hybrid_weight*sem_scores + (1-hybrid_weight)*lex_scores
        method = f"Hybrid ({hybrid_weight:.2f}*Semantic + {1-hybrid_weight:.2f}*BM25)"
    idxs = np.argsort(scores)[-5:][::-1]
    return [
        {**docs[i], "score": scores[i], "method": method}
        for i in idxs
    ]
