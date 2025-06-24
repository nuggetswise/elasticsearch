import streamlit as st
import openai

def get_openai_api_key():
    return st.secrets["openai_api_key"]

# --- Summarize job post into key sections ---
def summarize_job_post(job_post):
    openai.api_key = get_openai_api_key()
    prompt = f"""
Summarize the following Elastic job posting into:
- Responsibilities
- Key product areas
- Skills and requirements
- Metrics or KPIs (if mentioned)
Format each as a Markdown bullet list.

Job Posting:
{job_post}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.3,
    )
    text = response["choices"][0]["message"]["content"]
    # Simple parsing for demo; in production, use regex or structured output
    sections = {"responsibilities": "", "product_areas": "", "skills": "", "metrics": ""}
    for key in sections:
        idx = text.lower().find(key.replace('_', ' '))
        if idx != -1:
            next_idx = min([text.lower().find(k, idx+1) for k in sections if k != key and text.lower().find(k, idx+1) != -1] + [len(text)])
            sections[key] = text[idx+len(key)+1:next_idx].strip()
    return sections

# --- Simulate LLM response grounded in retrieved chunks ---
def simulate_llm_response(question, chunks):
    context = "\n\n".join(chunks)
    return f"You asked: {question}\n\nBased on Elastic’s job description and relevant context:\n\n{context}\n\n(Answer would be generated here by Nuggetwise LLM)"

# --- Agent insights (interview prep, strategy, etc) ---
def agent_insight_response(prompt, job_chunks):
    openai.api_key = get_openai_api_key()
    context = "\n\n".join(job_chunks)
    full_prompt = f"Job context:\n{context}\n\nPrompt: {prompt}\n\nGive a high-level, strategic answer that connects to the job post."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}],
        max_tokens=400,
        temperature=0.5,
    )
    return response["choices"][0]["message"]["content"]

# --- Fit summary LLM ---
def fit_summary_llm(resume_text, job_post):
    openai.api_key = get_openai_api_key()
    prompt = f"""
You are an expert career coach and product leader. Given the following job posting and resume, write a concise, personalized summary (in 5-8 bullet points) of why this candidate is a strong fit for the role. Highlight alignment in skills, experience, and impact. Use a confident, professional tone.

Job Posting:
{job_post}

Resume:
{resume_text}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.4,
    )
    return response["choices"][0]["message"]["content"]
