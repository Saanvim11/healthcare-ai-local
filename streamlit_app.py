import streamlit as st
import requests

st.set_page_config(page_title="🏥 MedAI", layout="wide")
st.title("🏥 MedAI - Local Healthcare AI Assistant")

BASE_URL = "http://localhost:8000"

if 'token' not in st.session_state:
    st.session_state.token = None

mode = st.sidebar.radio("Select Mode", ["Public (Anyone)", "Doctor Mode"])

# ====================== PUBLIC MODE ======================
if mode == "Public (Anyone)":
    st.header("🧑‍⚕️ Ask Any Medical Question")
    query = st.text_area("Your Question", placeholder="What are symptoms of diabetes?")

    if st.button("Get Answer", type="primary"):
        if query:
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(f"{BASE_URL}/clinical/reason", json={"query": query})
                    if resp.status_code == 200:
                        data = resp.json()
                        st.subheader("Answer")
                        st.write(data.get("answer", "No answer received"))
                        if data.get("precautions"):
                            st.subheader("Precautions")
                            st.write(data.get("precautions"))
                        st.caption(data.get("disclaimer", ""))
                    else:
                        st.error(f"Error: {resp.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

# ====================== DOCTOR MODE ======================
elif mode == "Doctor Mode":
    if not st.session_state.token:
        st.header("🔑 Doctor Login")
        username = st.text_input("Username", "doctor@example.com")
        password = st.text_input("Password", "password123", type="password")
        if st.button("Login"):
            r = requests.post(f"{BASE_URL}/auth/login", data={"username": username, "password": password})
            if r.status_code == 200:
                st.session_state.token = r.json()["access_token"]
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        st.success("Doctor Mode Active")
        patient_id = st.number_input("Patient ID", value=1, min_value=1)
        query = st.text_area("Patient Symptoms / Query")

        if st.button("Generate Clinical Note", type="primary"):
            with st.spinner("AI Reasoning..."):
                try:
                    headers = {'Authorization': f'Bearer {st.session_state.token}'}
                    resp = requests.post(
                        f"{BASE_URL}/clinical/reason",
                        json={"query": query, "patient_id": patient_id},
                        headers=headers
                    )
                    if resp.status_code == 200:
                        data = resp.json()

                        if "report" in data:
                            st.markdown(data["report"])   # This will show the full formatted report
                        else:
                            st.json(data)  # Fallback

                    else:
                        st.error(f"Error: {resp.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()

st.sidebar.caption("MedAI | Local & Private")