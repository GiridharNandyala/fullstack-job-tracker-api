import streamlit as st
import requests

# FastAPI Backend Base URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Job Application Tracker", layout="wide")

st.title("💼 Job Application Tracker Dashboard")

# Session State for Authentication Token
if "token" not in st.session_state:
    st.session_state["token"] = None

# --- SIDEBAR: AUTHENTICATION ---
st.sidebar.header("🔑 Authentication")

if not st.session_state["token"]:
    auth_mode = st.sidebar.radio("Choose Action", ["Login", "Register"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if auth_mode == "Register":
        if st.sidebar.button("Register Account"):
            response = requests.post(f"{API_URL}/register", json={"email": email, "password": password})
            if response.status_code == 201:
                st.sidebar.success("Account created successfully! Please Login.")
            else:
                st.sidebar.error(response.json().get("detail", "Registration failed"))

    elif auth_mode == "Login":
        if st.sidebar.button("Login"):
            response = requests.post(f"{API_URL}/login", data={"username": email, "password": password})
            if response.status_code == 200:
                token_data = response.json()
                st.session_state["token"] = token_data["access_token"]
                st.sidebar.success("Logged in successfully!")
                st.rerun()
            else:
                st.sidebar.error("Invalid email or password")
else:
    st.sidebar.success("Authenticated ✅")
    if st.sidebar.button("Logout"):
        st.session_state["token"] = None
        st.rerun()

# --- MAIN DASHBOARD (Protected) ---
if st.session_state["token"]:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    # Tab layout
    tab1, tab2 = st.tabs(["📋 View Jobs", "➕ Add New Job"])

    # TAB 1: VIEW & FILTER JOBS
    with tab1:
        st.subheader("Your Job Applications")
        
        status_filter = st.selectbox("Filter by Status", ["All", "Applied", "Interviewing", "Offered", "Rejected"])
        
        params = {}
        if status_filter != "All":
            params["status"] = status_filter

        res = requests.get(f"{API_URL}/jobs", headers=headers, params=params)
        
        if res.status_code == 200:
            jobs = res.json()
            if jobs:
                st.dataframe(jobs, use_container_width=True)
            else:
                st.info("No job applications found.")
        else:
            st.error("Failed to load jobs. Token might be expired.")

    # TAB 2: ADD JOB
    with tab2:
        st.subheader("Add a New Job Application")
        with st.form("add_job_form"):
            title = st.text_input("Job Title", placeholder="e.g. Data Analyst")
            company = st.text_input("Company Name", placeholder="e.g. Google")
            status = st.selectbox("Status", ["Applied", "Interviewing", "Offered", "Rejected"])
            submit = st.form_submit_button("Save Job")

            if submit:
                if title and company:
                    payload = {"title": title, "company": company, "status": status}
                    post_res = requests.post(f"{API_URL}/jobs", headers=headers, json=payload)
                    if post_res.status_code == 201:
                        st.success(f"Job at {company} saved successfully!")
                    else:
                        st.error("Failed to add job.")
                else:
                    st.warning("Please fill in all fields.")
else:
    st.warning("👈 Please Login or Register from the sidebar to access your tracker.")