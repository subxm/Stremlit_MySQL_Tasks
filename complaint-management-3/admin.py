import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shubham",
        database="complaint_db"
    )

st.set_page_config(page_title="Admin Panel", layout="wide")
st.sidebar.title("🔐 Admin Menu")

menu = st.sidebar.selectbox("Select Option", [
    "View All Complaints",
    "Search by Complaint ID"
])

conn = get_connection()
cursor = conn.cursor(dictionary=True)

if menu == "View All Complaints":
    st.title("📋 All Complaints")
    cursor.execute("SELECT * FROM complaints ORDER BY created_at DESC")
    complaints = cursor.fetchall()

    for c in complaints:
        with st.expander(f"Complaint ID: {c['id']} | Status: {c['status']}"):
            st.write(f"**Name:** {c['name']}")
            st.write(f"**Email:** {c['email']}")
            st.write(f"**Category:** {c['category']}")
            st.write(f"**Description:** {c['description']}")
            st.write(f"**Created At:** {c['created_at']}")

            new_status = st.selectbox(
                "Update Status",
                ["Open", "In Progress", "Closed"],
                index=["Open", "In Progress", "Closed"].index(c["status"]),
                key=c["id"]
            )

            if st.button("Update Status", key=f"btn{c['id']}"):
                cursor.execute(
                    "UPDATE complaints SET status=%s WHERE id=%s",
                    (new_status, c["id"])
                )
                conn.commit()
                st.success("Status Updated")

elif menu == "Search by Complaint ID":
    st.title("🔍 Search Complaint")
    cid = st.number_input("Enter Complaint ID", min_value=1)

    if st.button("Search"):
        cursor.execute("SELECT * FROM complaints WHERE id=%s", (cid,))
        c = cursor.fetchone()

        if c:
            st.subheader(f"Complaint ID: {c['id']}")
            st.write(f"**Name:** {c['name']}")
            st.write(f"**Email:** {c['email']}")
            st.write(f"**Category:** {c['category']}")
            st.write(f"**Description:** {c['description']}")
            st.write(f"**Status:** {c['status']}")
        else:
            st.error("Complaint Not Found")

conn.close()
