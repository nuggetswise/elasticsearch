import streamlit as st

def render():
    st.header("💼 My Fit")
    st.markdown("""
### Why I'm a Strong Candidate for Elastic

- **Proven Revenue Impact:** Led AI product launches driving $XM+ in new ARR and double-digit adoption growth.
- **Platform Thinking:** Built and scaled ingestion pipelines, hybrid search, and developer-facing APIs—directly aligned with Elastic’s platform vision.
- **AI & Search Expertise:** Designed and shipped RAG systems (Nuggetwise), integrating LLMs, semantic/lexical retrieval, and editorial voice preservation.
- **Customer-Centric Roadmaps:** Shipped features with measurable NPS gains by deeply collaborating with customers and field teams.
- **Developer Empathy:** Advocated for docs, SDKs, and DX improvements that reduced integration time by 40%+.
- **Elastic Alignment:** Experience with search, ingestion, LLMs, and AI product design matches Elastic’s focus on platform, observability, and search innovation.

> "I bring a unique blend of technical depth, product strategy, and a track record of shipping AI-powered search experiences at scale—making me an ideal fit for Elastic’s next phase."
    """)
    st.subheader("🤖 LLM-Generated Fit Summary (Bonus)")
    uploaded_file = st.file_uploader("Upload your PDF resume for a personalized fit summary:", type=["pdf"], key="fit_pdf")
    if uploaded_file:
        import PyPDF2
        from utils.llm import fit_summary_llm
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = "\n".join(page.extract_text() or '' for page in reader.pages)
            if not resume_text.strip():
                st.warning("No text could be extracted from the PDF.")
            else:
                job_post = load_job_post()
                with st.spinner("Generating fit summary with LLM..."):
                    summary = fit_summary_llm(resume_text, job_post)
                st.markdown("**LLM Fit Summary:**")
                st.success(summary)
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
