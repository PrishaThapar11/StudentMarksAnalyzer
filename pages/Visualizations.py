import streamlit as st
import pandas as pd
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #8AB4F8 0%, #9fb9ed 100%) !important;
        }
        .block-container {
            background: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

import plotly.express as px
from utils.login import require_login
require_login()

st.title("📈 Visualizations Dashboard")



if "all_classes_data" not in st.session_state or not st.session_state["all_classes_data"]:
    st.warning("⚠ Please upload CSVs first in **Upload & Analyze** page.")
    st.stop()

selected_class = st.selectbox(
    "Select Class",
    list(st.session_state["all_classes_data"].keys())
)

df = st.session_state["all_classes_data"][selected_class]


subjects = ['Math','Science','English','History','Computer']

# -------------------------
# Bar Chart – Subject-wise Average
# -------------------------
st.subheader("📘 Subject-wise Average Marks (Bar Chart)")
subj_avg = df[subjects].mean().reset_index()
subj_avg.columns = ["Subject", "Average Marks"]

fig_bar = px.bar(subj_avg, x="Subject", y="Average Marks", title="Average Marks per Subject")
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------
# Histogram – Percentage Distribution
# -------------------------
st.subheader("📊 Percentage Distribution (Histogram)")

fig_hist = px.histogram(df, x="Percentage", nbins=10, title="Distribution of Class Percentages")
st.plotly_chart(fig_hist, use_container_width=True)

# -------------------------
# Boxplot – Subject-wise Distribution
# -------------------------
st.subheader("📦 Boxplot of Marks per Subject")

df_melted = df.melt(id_vars=["Roll","Name"], value_vars=subjects,
                    var_name="Subject", value_name="Marks")

fig_box = px.box(df_melted, x="Subject", y="Marks", title="Marks Distribution by Subject")
st.plotly_chart(fig_box, use_container_width=True)

