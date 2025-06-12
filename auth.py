# auth.py
import streamlit as st

# Optional: You can store these in environment variables for better security
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def admin_login():
    st.sidebar.title("🔐 Admin Login")
    
    # Initialize session state if not set
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    if not st.session_state["admin_logged_in"]:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        login_btn = st.sidebar.button("Login")

        if login_btn:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state["admin_logged_in"] = True
                st.sidebar.success("✅ Login successful!")
            else:
                st.sidebar.error("❌ Invalid credentials")
    else:
        st.sidebar.success("✅ Logged in as admin")
        if st.sidebar.button("Logout"):
            st.session_state["admin_logged_in"] = False
            st.rerun()

    return st.session_state["admin_logged_in"]
