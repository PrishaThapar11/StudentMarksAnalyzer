import streamlit as st

# ------------------------
# Global Styling
# ------------------------
st.markdown("""
    <style>
        /* Page Background */
        [data-testid="stAppViewContainer"] {
    background-color: #9fb9ed !important;  /* soft blue */
    background-image: linear-gradient(135deg, #9fb9ed, #dbe9f7);  /* optional gradient */
}
/* All main content cards */
[data-testid="stBlock"] {
    background-color: rgba(255, 255, 255, 0.85) !important;  /* semi-transparent white */
    color: #1A237E !important;  /* dark font */
    border-radius: 12px !important;
    padding: 1rem !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* DataFrames / tables */
.stDataFrame {
    background-color: #E3F2FD !important;  /* light blue table background */
    color: #1A237E !important;
    border-radius: 8px !important;
}


        /* Titles */
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif !important;
            color: #1A237E !important;
        }

        /* Generic text */
        body, p, label {
            font-family: 'Segoe UI', sans-serif !important;
        }

        /* Buttons */
        .stButton>button {
            color: white !important;
            background: linear-gradient(135deg, #5C6BC0, #283593) !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.2rem !important;
            border: none !important;
            font-size: 16px !important;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.2);
        }

        /* Button on hover */
        .stButton>button:hover {
            background: linear-gradient(135deg, #3F51B5, #1A237E) !important;
        }

        /* Input fields */
        .stTextInput>div>div>input {
            background-color: #FFFFFF !important;
            border-radius: 8px !important;
            border: 1px solid #C5CAE9 !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #E8EAF6;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------
# App Config
# ------------------------
st.set_page_config(page_title="Student Marks Analyzer", layout="wide")

# ------------------------
# SIGNUP PAGE
# ------------------------
def signup():
    st.title("📝 Create an Account")

    new_username = st.text_input("✨ Create Username")
    new_password = st.text_input("🔑 Create Password", type="password")

    if st.button("Sign Up"):
        if new_username and new_password:
            st.session_state["registered_username"] = new_username
            st.session_state["registered_password"] = new_password

            st.success("🎉 Account created successfully! Please login now.")
            st.session_state["show_signup"] = False
            st.rerun()
        else:
            st.error("⚠ Username and Password cannot be empty.")

    if st.button("Already have an account? Login"):
        st.session_state["show_signup"] = False
        st.rerun()

# ------------------------
# LOGIN PAGE
# ------------------------
def login():
    st.title("🔐 Login to Continue")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        if "registered_username" not in st.session_state:
            st.error("⚠ No user registered yet. Please sign up first.")
            return

        if username == st.session_state["registered_username"] and password == st.session_state["registered_password"]:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

    st.write("Don't have an account?")
    if st.button("Go to Sign Up"):
        st.session_state["show_signup"] = True
        st.rerun()

# ------------------------
# HOME PAGE
# ------------------------
def home_page():
    st.sidebar.title("📌 Navigation")
    st.sidebar.info("Use the menu to explore features")

    st.title(f"🎓 Welcome, **{st.session_state['registered_username']}**!")
    st.subheader("Here's what you can do in this app:")

    st.markdown("""
    ### 📚 Features Available:
    - **📤 Upload & Analyze:** Upload a CSV and calculate totals, percentage, grades.
    - **📊 Class Analytics:** View class averages, top performers, subject strength.
    - **📈 Visualizations:** Bar charts, histograms & boxplots.
    - **👤 Student Report:** Generate a detailed report card.

    Use the sidebar on the left to navigate between features.
    """)

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["show_signup"] = True
        st.rerun()

# ------------------------
# MAIN LOGIC
# ------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = True

if st.session_state["logged_in"]:
    home_page()
elif st.session_state["show_signup"]:
    signup()
else:
    login()
