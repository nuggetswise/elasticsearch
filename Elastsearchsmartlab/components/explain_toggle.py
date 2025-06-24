import streamlit as st

def explain_toggle():
    st.markdown("**🤖 AI-Powered Insights**")
    explain = st.toggle(
        "Enable AI Explanation", 
        value=False,
        help="Get an AI-powered explanation of how different search strategies work. This will show you the pros and cons of each approach."
    )
    
    if explain:
        st.info("""
        **AI Explanation Enabled!** 
        
        After running a search, you'll see an AI-generated explanation that covers:
        - How each search strategy works
        - Pros and cons of different approaches  
        - When to use each method
        - Real-world applications
        """)
    
    return explain
