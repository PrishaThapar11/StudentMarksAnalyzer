import streamlit as st
from utils.login import require_login
st.markdown(
    """
    <style>
        /* Change entire page background */
        .stApp {
            background-color: #b5cbf7 !important;
        }

        /* Change main content area background */
        .block-container {
            background-color: #b5cbf7 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

require_login()

st.title("👤 Student Report Generator")



if "all_classes_data" not in st.session_state or not st.session_state["all_classes_data"]:
    st.warning("⚠ Please upload CSVs first in **Upload & Analyze** page.")
    st.stop()

selected_class = st.selectbox(
    "Select Class",
    list(st.session_state["all_classes_data"].keys())
)

df = st.session_state["all_classes_data"][selected_class]


# Select student
student_name = st.selectbox("Select a student", df["Name"].unique())

if student_name:
    student = df[df["Name"] == student_name].iloc[0]

    st.subheader(f"📄 Report Card: {student['Name']}")
    st.write(f"**Roll Number:** {student['Roll']}")

    # Subject-wise marks
    st.subheader("📝 Subject Marks")
    marks = student[["Math", "Science", "English", "History", "Computer"]]
    st.write(marks)

    # Total, Percentage, Grade
    st.subheader("📊 Performance Summary")
    st.write(f"**Total Marks:** {student['Total']}")
    st.write(f"**Percentage:** {student['Percentage']:.2f}%")
    st.write(f"**Grade:** {student['Grade']}")

    # Remarks
    st.subheader("🗒 Teacher Remarks")
    if student["Percentage"] >= 90:
        remark = "Outstanding performance! Keep it up!"
    elif student["Percentage"] >= 75:
        remark = "Very good work! Aim for even higher."
    elif student["Percentage"] >= 60:
        remark = "Good effort. You can improve further."
    else:
        remark = "Needs improvement. Consistent study required."

    st.info(remark)

