import numpy as np
from sentence_transformers import SentenceTransformer
import streamlit as st
from utils.dummy_docs import DOCS
from rank_bm25 import BM25Okapi
import os

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
    # Try lunr.py (Python port of lunr.js) first, fallback to BM25
    try:
        from lunr import lunr
        # Build lunr index
        documents = [
            {"id": str(i), "title": doc["title"], "snippet": doc["snippet"]}
            for i, doc in enumerate(docs)
        ]
        idx = lunr(ref="id", fields=("title", "snippet"), documents=documents)
        results = idx.search(query)
        # Map lunr results to scores (normalize to 0-1)
        score_map = {r['ref']: r['score'] for r in results}
        max_score = max(score_map.values()) if score_map else 1.0
        scores = [score_map.get(str(i), 0.0)/max_score for i in range(len(docs))]
        return np.array(scores)
    except Exception:
        # Fallback to BM25
        tokenized_corpus = [doc['snippet'].lower().split() for doc in docs]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = query.lower().split()
        scores = bm25.get_scores(tokenized_query)
        # Normalize BM25 scores to 0-1
        max_score = max(scores) if len(scores) > 0 else 1.0
        return np.array(scores) / max_score

def get_semantic_scores(query, docs):
    # Try Cohere embeddings first, fallback to sentence-transformers
    try:
        import cohere
        cohere_key = st.secrets.get("cohere_api_key", None) or os.environ.get("COHERE_API_KEY") or os.environ.get("cohere_api_key")
        if cohere_key:
            co = cohere.Client(cohere_key)
            texts = [doc["title"] for doc in docs]
            doc_embs = co.embed(texts=texts, model="embed-english-v3.0").embeddings
            q_emb = co.embed(texts=[query], model="embed-english-v3.0").embeddings[0]
            doc_embs = np.array(doc_embs)
            q_emb = np.array(q_emb)
            scores = np.dot(doc_embs, q_emb) / (np.linalg.norm(doc_embs, axis=1) * np.linalg.norm(q_emb) + 1e-8)
            return scores
    except Exception:
        pass
    # Fallback to sentence-transformers
    titles = [doc["title"] for doc in docs]
    doc_embs = embed_texts(titles)
    q_emb = embed_texts([query])[0]
    scores = np.dot(doc_embs, q_emb) / (np.linalg.norm(doc_embs, axis=1) * np.linalg.norm(q_emb) + 1e-8)
    return scores

def get_llm_scores(query, docs):
    import openai
    scores = []
    # Try OpenAI
    try:
        api_key = st.secrets.get("openai_api_key", None) or os.environ.get("OPENAI_API_KEY") or os.environ.get("openai_api_key")
        if api_key:
            openai.api_key = api_key
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
    except Exception:
        pass
    # Try Cohere
    try:
        import cohere
        cohere_key = st.secrets.get("cohere_api_key", None) or os.environ.get("COHERE_API_KEY") or os.environ.get("cohere_api_key")
        if cohere_key:
            co = cohere.Client(cohere_key)
            for doc in docs:
                prompt = f"Given the query: '{query}', rate the relevance of the following document (0-1):\nTitle: {doc['title']}\nSnippet: {doc['snippet']}"
                try:
                    resp = co.generate(
                        model="command-r-plus",
                        prompt=prompt,
                        max_tokens=10,
                        temperature=0.0,
                    )
                    text = resp.generations[0].text.strip()
                    score = float(text.split()[0]) if text.split() else 0.0
                except Exception:
                    score = 0.0
                scores.append(score)
            return np.array(scores)
    except Exception:
        pass
    # Try Groq
    try:
        import requests
        groq_key = st.secrets.get("groq_api_key", None) or os.environ.get("GROQ_API_KEY") or os.environ.get("groq_api_key")
        if groq_key:
            for doc in docs:
                prompt = f"Given the query: '{query}', rate the relevance of the following document (0-1):\nTitle: {doc['title']}\nSnippet: {doc['snippet']}"
                try:
                    response = requests.post(
                        "https://api.groq.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                        json={
                            "model": "llama3-70b-8192",
                            "messages": [{"role": "user", "content": prompt}],
                            "max_tokens": 10,
                            "temperature": 0.0
                        },
                        timeout=10
                    )
                    text = response.json()["choices"][0]["message"]["content"].strip()
                    score = float(text.split()[0]) if text.split() else 0.0
                except Exception:
                    score = 0.0
                scores.append(score)
            return np.array(scores)
    except Exception:
        pass
    # Try Gemini
    try:
        import google.generativeai as genai
        gemini_key = st.secrets.get("gemini_api_key", None) or os.environ.get("GEMINI_API_KEY") or os.environ.get("gemini_api_key")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            for doc in docs:
                prompt = f"Given the query: '{query}', rate the relevance of the following document (0-1):\nTitle: {doc['title']}\nSnippet: {doc['snippet']}"
                try:
                    resp = model.generate_content(prompt)
                    text = resp.text.strip()
                    score = float(text.split()[0]) if text.split() else 0.0
                except Exception:
                    score = 0.0
                scores.append(score)
            return np.array(scores)
    except Exception:
        pass
    # If all fail, return zeros
    return np.zeros(len(docs))

def get_simulated_results(query, mode, filters=None, hybrid_weight=0.6, user_docs=None):
    docs = user_docs if user_docs is not None else DOCS
    docs = filter_docs(docs, filters)
    if not docs:
        return []
    if mode == "Lexical":
        scores = get_bm25_scores(query, docs)
        method = "Lunr.js (Python) or BM25 fallback"
    elif mode == "Semantic":
        scores = get_semantic_scores(query, docs)
        method = "Cohere Embedding (fallback: sentence-transformers)"
    elif mode == "LLM":
        scores = get_llm_scores(query, docs)
        method = "LLM (OpenAI→Cohere→Groq→Gemini)"
    else:  # Hybrid
        sem_scores = get_semantic_scores(query, docs)
        lex_scores = get_bm25_scores(query, docs)
        scores = hybrid_weight*sem_scores + (1-hybrid_weight)*lex_scores
        method = f"Hybrid (Semantic + Lexical)"
    idxs = np.argsort(scores)[-5:][::-1]
    return [
        {**docs[i], "score": scores[i], "method": method}
        for i in idxs
    ]
