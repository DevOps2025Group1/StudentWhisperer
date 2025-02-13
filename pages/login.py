import streamlit as st
import pyodbc
import pandas as pd

@st.cache_resource
def init_connection():
    connection_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=" + st.secrets["server"] + ";"
        "DATABASE=" + st.secrets["database"] + ";"
        "UID=" + st.secrets["username"] + ";"
        "PWD=" + st.secrets["password"]
    )
    return pyodbc.connect(connection_str)

conn = init_connection()

def main():
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

if __name__ == '__main__':
    main()
