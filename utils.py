import streamlit as st
import pyodbc

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
