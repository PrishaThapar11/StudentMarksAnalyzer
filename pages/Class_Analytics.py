
import streamlit as st
import pandas as pd
st.markdown(
    """
    <style>
        /* Change entire page background */
        .stApp {
            background-color: #97c2e8 !important;
        }

        /* Change main content area background */
        .block-container {
            background-color: #97c2e8 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

from utils.login import require_login
require_login()


if "all_classes_data" not in st.session_state or not st.session_state["all_classes_data"]:
    st.warning("⚠ Please upload CSVs first in **Upload & Analyze** page.")
    st.stop()

selected_class = st.selectbox(
    "Select Class",
    list(st.session_state["all_classes_data"].keys())
)

df = st.session_state["all_classes_data"][selected_class]


st.title("📊 Class Analytics")



# ------------------------
# Basic Stats
# ------------------------
st.subheader("📌 Overall Class Performance")

st.write(f"**Number of Students:** {df.shape[0]}")
st.write(f"**Class Average (%):** {df['Percentage'].mean():.2f}")
st.write(f"**Highest Score:** {df['Total'].max()} ({df.loc[df['Total'].idxmax(), 'Name']})")
st.write(f"**Lowest Score:** {df['Total'].min()} ({df.loc[df['Total'].idxmin(), 'Name']})")

# ------------------------
# Subject-wise Averages
# ------------------------
st.subheader("📘 Subject-wise Performance")

subjects = ['Math','Science','English','History','Computer']
subject_avgs = df[subjects].mean().reset_index()
subject_avgs.columns = ['Subject', 'Average Marks']

st.dataframe(subject_avgs)

# ------------------------
# Leaderboard
# ------------------------
st.subheader("🏆 Top 10 Students")

top_students = df.sort_values(by="Total", ascending=False).head(10)
st.dataframe(top_students[['Roll','Name','Total','Percentage','Grade']])
