import streamlit as st
import psycopg2

def connect_to_database():
    try:
        connection = psycopg2.connect(
            host=st.secrets["DB_HOST"],
            database=st.secrets["DB_NAME"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            port=st.secrets["DB_PORT"],
            sslmode="require"
        )
        return connection

    except Exception as e:
        print(e)
        return None