import streamlit as st
from sections import role_explorer, nuggetwise_simulator, agent_insights, my_fit

st.set_page_config(page_title="Nuggetwise x Elastic: Role Explorer", layout="wide")

st.sidebar.title("Nuggetwise x Elastic")
section = st.sidebar.radio(
    "Go to section:",
    [
        "🧭 Role Explorer",
        "🔍 Nuggetwise Simulator",
        "🧠 Agent Insights",
        "💼 My Fit"
    ]
)

if section == "🧭 Role Explorer":
    role_explorer.render()
elif section == "🔍 Nuggetwise Simulator":
    nuggetwise_simulator.render()
elif section == "🧠 Agent Insights":
    agent_insights.render()
elif section == "💼 My Fit":
    my_fit.render()
