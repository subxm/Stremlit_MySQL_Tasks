import streamlit as st
import mysql.connector
import re

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shubham",
        database="complaint_db"
    )

st.set_page_config(page_title="Complaint Portal", layout="centered")
st.title("📝 Online Complaint Registration")

name = st.text_input("Name")
email = st.text_input("Email")
category = st.selectbox("Category", ["Technical", "Billing", "Service", "Other"])
description = st.text_area("Complaint Description")

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

if st.button("Submit Complaint"):
    if not name or not email or not description:
        st.error("All fields are required")
    elif not valid_email(email):
        st.error("Invalid email format")
    else:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO complaints (name, email, category, description) VALUES (%s,%s,%s,%s)",
            (name, email, category, description)
        )
        conn.commit()
        complaint_id = cursor.lastrowid
        conn.close()

        st.success(f"Complaint Submitted Successfully!")
        st.info(f"Your Complaint ID: {complaint_id}")
