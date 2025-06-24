import streamlit as st
from utils.retrieval import get_simulated_results

def results_display(query, filters=None, hybrid_weight=0.6, user_docs=None):
    modes = ["Lexical", "Semantic", "Hybrid", "LLM"]
    cols = st.columns(len(modes))
    for idx, m in enumerate(modes):
        with cols[idx]:
            st.markdown(f"#### {m}")
            results = get_simulated_results(query, m, filters=filters, hybrid_weight=hybrid_weight, user_docs=user_docs)
            filtered_results = [r for r in results if r['score'] >= 0.30]
            if not filtered_results:
                st.info("No results.")
                continue
            for i, res in enumerate(filtered_results, 1):
                st.write(f"**{i}. {res['title']}** — Score: {res['score']:.2f}")
                st.caption(res['snippet'][:100] + ("..." if len(res['snippet']) > 100 else ""))
                st.markdown(f"*Author:* {res['author']} | *Date:* {res['date']}")
                st.markdown(f"_Method: {res['method']}_")
                st.markdown("---")
