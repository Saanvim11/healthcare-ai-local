import streamlit as st

st.set_page_config(page_title="MedAI", layout="wide")
st.title("🏥 MedAI - Healthcare AI Assistant")
st.write("### Backend Integration Test")

if st.button("Test Clinical Reasoning"):
    st.success("✅ Button works! Integration is active.")
    st.info("If you see this message, the frontend is working.")

st.sidebar.info("Phase 5 Integration - Basic Version")