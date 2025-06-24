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
        try:
            import cohere
            co = cohere.Client(st.secrets["cohere_api_key"])
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
        except Exception:
            yield "[LLM unavailable: Could not explain retrieval strategy.]"
