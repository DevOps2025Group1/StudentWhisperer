"""
This module renders the Student Profile page using Streamlit. It displays the
student's profile information, courses, and grades. It also provides a
logout button to clear the session state.
"""

import streamlit as st
import pandas as pd
import utils

conn = utils.init_connection()

def main():
    st.title("Student Profile")

    if "student_id" not in st.session_state:
        st.error("You must be logged in to view your profile. Please go to the Login page.")
        st.stop()

    student_id = st.session_state["student_id"]

    query_profile = """
    SELECT s.id AS student_id, s.name AS student_name, p.name AS program_name
    FROM Student s
    JOIN Program p ON s.program_id = p.id
    WHERE s.id = ?
    """
    df_profile = pd.read_sql(query_profile, conn, params=(int(student_id),))
    if not df_profile.empty:
        st.subheader("Profile Information")
        st.write(f"**Name:** {df_profile.iloc[0]['student_name']}")
        st.write(f"**Student ID:** {df_profile.iloc[0]['student_id']}")
        st.write(f"**Program:** {df_profile.iloc[0]['program_name']}")
    else:
        st.error("Student information not found.")

    query_courses = """
    SELECT c.name AS course_name, g.grade
    FROM Course c
    JOIN Grade g ON c.id = g.course_id
    WHERE g.student_id = ?
    """
    df_courses = pd.read_sql(query_courses, conn, params=(int(student_id),))
    if not df_courses.empty:
        st.subheader("Courses and Grades")
        st.table(df_courses[['course_name', 'grade']])
    else:
        st.info("No courses found for this student.")

    if st.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Logged out. Please go to the Login page to log in again.")

if __name__ == '__main__':
    main()
