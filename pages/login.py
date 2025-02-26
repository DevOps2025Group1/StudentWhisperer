"""
This module provides a login page for the StudentWhisperer application using Streamlit.
"""

import streamlit as st
import pandas as pd
from clients.utils import init_connection

conn = init_connection()


def main():
    """Render the login page and handle user authentication."""
    st.title("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        query = "SELECT id, name FROM Student WHERE email = ? AND password = ?"
        df = pd.read_sql(query, conn, params=(email, password))
        if not df.empty:
            st.session_state["student_id"] = df.iloc[0]["id"]
            st.session_state["student_name"] = df.iloc[0]["name"]
            st.success(f"Welcome, {df.iloc[0]['name']}!")
        else:
            st.error("Invalid email or password.")


if __name__ == "__main__":
    main()
