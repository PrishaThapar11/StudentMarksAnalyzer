import streamlit as st
import pandas as pd



# --------------------------
# GLOBAL PAGE STYLING (lightweight)
# --------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&display=swap');
        /* App background */
        .main {
            background-color: #9fb9ed !important;
        }
                /* Change entire page background */
        .stApp {
            background-color: #9fb9ed !important;
        }

        /* Change main content area background */
        .block-container {
            background-color: #9fb9ed !important;
        }
        /* Global font */
        * {
            font-family: 'Nunito', sans-serif !important;
        }

        /* Headings color */
        h1, h2, h3, h4, h5 {
            color: #041430 !important;
        }

        /* Paragraphs and labels */
        p, label, span {
            color: #34495E !important;
            font-size: 16px !important;
        }

        /* Text Inputs */
        .stTextInput>div>div>input {
            border-radius: 8px !important;
            border: 1px solid #AAB7B8 !important;
            background-color: white !important;
            padding: 6px 10px !important;
        }

        /* Number Inputs */
        .stNumberInput>div>div>input {
            border-radius: 8px !important;
            border: 1px solid #AAB7B8 !important;
            background-color: white !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #b2d7f7 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            font-size: 16px !important;
            border: none !important;
        }

        .stButton>button:hover {
            background-color: #303F9F !important;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #E8EAF6 !important;
        }

    </style>
""", unsafe_allow_html=True)

def calc_grade(p):
    if p >= 90: return "A+"
    elif p >= 80: return "A"
    elif p >= 70: return "B"
    elif p >= 60: return "C"
    else: return "D"

st.title("📤 Upload & Analyze Multiple Classes")

# Initialize storage for all class data
st.session_state.setdefault("all_classes_data", {})

# ======================================================
# 1️⃣ OPTION A: UPLOAD CSV FILES FOR MULTIPLE CLASSES
# ======================================================
st.header("📁 Upload Class CSV Files")

uploaded_files = st.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info("Assign a class name to each uploaded CSV and process it.")

    for uploaded_file in uploaded_files:
        class_label = st.text_input(
            f"Enter class name for {uploaded_file.name}",
            value=uploaded_file.name.replace(".csv", "")
        )

        if st.button(f"Process CSV: {class_label}", key=uploaded_file.name):
            try:
                df = pd.read_csv(uploaded_file)

                expected_columns = ['Roll','Name','Math','Science','English','History','Computer']

                if all(col in df.columns for col in expected_columns):
                    df.fillna(0, inplace=True)
                    df["Total"] = df[['Math','Science','English','History','Computer']].sum(axis=1)
                    df["Percentage"] = df["Total"] / 5
                    df["Grade"] = df["Percentage"].apply(calc_grade)

                    # Save processed data
                    st.session_state["all_classes_data"][class_label] = df
                    df.to_csv(f"data/{class_label}.csv", index=False)

                    st.success(f"Class **{class_label}** uploaded & processed successfully!")

                else:
                    st.error(f"CSV must contain columns: {expected_columns}")

            except Exception as e:
                st.error(f"Error processing file: {e}")

# ======================================================
# 2️⃣ OPTION B: MANUAL ENTRY FOR A CLASS
# ======================================================
st.header("✏️ Manually Enter Class Data")

with st.form("manual_entry_form"):
    manual_class_name = st.text_input("Enter Class Name")

    num_students = st.number_input(
        "How many students?",
        min_value=1,
        max_value=100,
        step=1
    )

    st.write("### Enter Student Details")

    student_entries = []
    for i in range(num_students):
        st.write(f"#### Student {i+1}")

        name = st.text_input(f"Name of Student {i+1}", key=f"name_{i}")
        math = st.number_input(f"Math Marks for {name}", key=f"math_{i}", min_value=0, max_value=100)
        science = st.number_input(f"Science Marks for {name}", key=f"sci_{i}", min_value=0, max_value=100)
        english = st.number_input(f"English Marks for {name}", key=f"eng_{i}", min_value=0, max_value=100)
        history = st.number_input(f"History Marks for {name}", key=f"hist_{i}", min_value=0, max_value=100)
        computer = st.number_input(f"Computer Marks for {name}", key=f"comp_{i}", min_value=0, max_value=100)

        student_entries.append({
            "Name": name,
            "Math": math,
            "Science": science,
            "English": english,
            "History": history,
            "Computer": computer
        })

    submit_manual = st.form_submit_button("Process Manual Entry")

# When submitted
if submit_manual:
    if manual_class_name.strip() == "":
        st.error("Class name cannot be empty!")
    else:
        df = pd.DataFrame(student_entries)

        # Generate Roll numbers automatically
        df.insert(0, "Roll", range(1, len(df)+1))

        # Create metrics
        df["Total"] = df[['Math','Science','English','History','Computer']].sum(axis=1)
        df["Percentage"] = df["Total"] / 5
        df["Grade"] = df["Percentage"].apply(calc_grade)

        # Save to session
        st.session_state["all_classes_data"][manual_class_name] = df

        # Save file
        df.to_csv(f"data/{manual_class_name}.csv", index=False)

        st.success(f"Class **{manual_class_name}** added successfully (Manual Entry)!")

# ======================================================
# SHOW ALL AVAILABLE CLASSES
# ======================================================
st.write("### 📚 Classes Processed:")
st.write(list(st.session_state["all_classes_data"].keys()))

