"""
Python utils used for pages.
"""

import streamlit as st
import pyodbc


@st.cache_resource
def init_connection():
    """Initialize and return a database connection using credentials from st.secrets."""  # noqa: E501
    connection_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=" + st.secrets["server"] + ";"
        "DATABASE=" + st.secrets["database"] + ";"
        "UID=" + st.secrets["username"] + ";"
        "PWD=" + st.secrets["password"]
    )
    return pyodbc.connect(connection_str)
