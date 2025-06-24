import streamlit as st
import openai
import time
import os

def explain_retrieval_strategy_stream(mode):
    prompt = f"""
Explain in 3-5 sentences, for a developer audience, how a '{mode}' search mode works in a modern search system. Include the pros, cons, and typical use cases. Use clear, technical language.
"""
    try:
        openai_key = st.secrets.get("openai_api_key", None) or os.environ.get("OPENAI_API_KEY") or os.environ.get("openai_api_key")
        if openai_key:
            openai.api_key = openai_key
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3,
                stream=True
            )
            buffer = ""
            for chunk in response:
                delta = chunk['choices'][0]['delta']
                if 'content' in delta:
                    buffer += delta['content']
                    yield delta['content']
                    time.sleep(0.05)
            if buffer:
                return
    except Exception as e:
        yield f"[OpenAI error: {e}]"
    try:
        import cohere
        cohere_key = st.secrets.get("cohere_api_key", None) or os.environ.get("COHERE_API_KEY") or os.environ.get("cohere_api_key")
        if cohere_key:
            co = cohere.Client(cohere_key)
            resp = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=200,
                temperature=0.3,
            )
            text = resp.generations[0].text.strip()
            if text:
                for sent in text.split('.'):
                    if sent.strip():
                        yield sent.strip() + '.'
                        time.sleep(0.1)
                return
    except Exception as e:
        yield f"[Cohere error: {e}]"
    try:
        import requests
        groq_key = st.secrets.get("groq_api_key", None) or os.environ.get("GROQ_API_KEY") or os.environ.get("groq_api_key")
        if groq_key:
            groq_resp = requests.post(
                "https://api.groq.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                json={
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 200,
                    "temperature": 0.3
                },
                timeout=10
            )
            try:
                text = groq_resp.json()["choices"][0]["message"]["content"].strip()
                if text:
                    for sent in text.split('.'):
                        if sent.strip():
                            yield sent.strip() + '.'
                            time.sleep(0.1)
                    return
            except Exception as e:
                yield f"[Groq response error: {e}]"
    except Exception as e:
        yield f"[Groq error: {e}]"
    try:
        import google.generativeai as genai
        gemini_key = st.secrets.get("gemini_api_key", None) or os.environ.get("GEMINI_API_KEY") or os.environ.get("gemini_api_key")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-pro')
            resp = model.generate_content(prompt)
            text = resp.text.strip()
            if text:
                for sent in text.split('.'):
                    if sent.strip():
                        yield sent.strip() + '.'
                        time.sleep(0.1)
                return
    except Exception as e:
        yield f"[Gemini error: {e}]"
    yield ("[LLM unavailable: Could not explain retrieval strategy.\n\n" \
           "Typical LLM usage: LLMs can be used to explain, summarize, or re-rank search results, "
           "provide natural language answers, or generate explanations for retrieval strategies. "
           "If you see this message, it means no LLM provider is available, misconfigured, or all failed.")
