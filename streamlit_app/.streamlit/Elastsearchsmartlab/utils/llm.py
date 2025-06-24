import streamlit as st
import openai
import time

def explain_retrieval_strategy_stream(mode):
    prompt = f"""
Explain in 3-5 sentences, for a developer audience, how a '{mode}' search mode works in a modern search system. Include the pros, cons, and typical use cases. Use clear, technical language.
"""
    try:
        openai.api_key = st.secrets["openai_api_key"]
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
        if not buffer:
            yield "[No content returned from LLM]"
    except Exception:
        # Try Cohere
        try:
            import cohere
            cohere_key = st.secrets["cohere_api_key"]
            if cohere_key:
                co = cohere.Client(cohere_key)
                resp = co.generate(
                    model="command-r-plus",
                    prompt=prompt,
                    max_tokens=200,
                    temperature=0.3,
                )
                for sent in resp.generations[0].text.strip().split('.'):
                    if sent.strip():
                        yield sent.strip() + '.'
                        time.sleep(0.1)
                return
        except Exception:
            pass
        # Try Groq
        try:
            import requests
            groq_key = st.secrets["groq_api_key"]
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
                text = groq_resp.json()["choices"][0]["message"]["content"].strip()
                for sent in text.split('.'):
                    if sent.strip():
                        yield sent.strip() + '.'
                        time.sleep(0.1)
                return
        except Exception:
            pass
        # Try Gemini
        try:
            import google.generativeai as genai
            gemini_key = st.secrets["gemini_api_key"]
            if gemini_key:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-pro')
                resp = model.generate_content(prompt)
                text = resp.text.strip()
                for sent in text.split('.'):
                    if sent.strip():
                        yield sent.strip() + '.'
                        time.sleep(0.1)
                return
        except Exception:
            pass
        fallback_message = "LLM unavailable: Could not explain retrieval strategy.\n\nTypical LLM usage: LLMs can be used to explain, summarize, or re-rank search results, provide natural language answers, or generate explanations for retrieval strategies. If you see this message, it means no LLM provider is available or configured."
        yield fallback_message
