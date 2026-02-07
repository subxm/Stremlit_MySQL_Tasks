import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DB CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shubham",   # <-- your password
        database="student_db"
    )

# ---------------- FUNCTIONS ----------------
def add_student(name, age, subject, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, subject, marks) VALUES (%s,%s,%s,%s)",
        (name, age, subject, marks)
    )
    conn.commit()
    conn.close()

def fetch_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

def update_marks(student_id, marks):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET marks=%s WHERE id=%s", (marks, student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()

# ---------------- UI ----------------
st.set_page_config(page_title="Student Performance", layout="wide")
st.title("🎓 Student Performance Management System")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "View Students", "Update Marks", "Delete Student", "Analysis"]
)

# ---------------- ADD STUDENT ----------------
if menu == "Add Student":
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    subject = st.text_input("Subject")
    marks = st.number_input("Marks", min_value=0, max_value=100)

    if st.button("Add Student"):
        add_student(name, age, subject, marks)
        st.success("Student added successfully")

# ---------------- VIEW STUDENTS ----------------
elif menu == "View Students":
    df = fetch_data()
    if df.empty:
        st.warning("No records found")
    else:
        df["Result"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")
        st.dataframe(df)

# ---------------- UPDATE ----------------
elif menu == "Update Marks":
    student_id = st.number_input("Student ID", min_value=1)
    marks = st.number_input("New Marks", min_value=0, max_value=100)
    if st.button("Update Marks"):
        update_marks(student_id, marks)
        st.success("Marks updated")

# ---------------- DELETE ----------------
elif menu == "Delete Student":
    student_id = st.number_input("Student ID", min_value=1)
    if st.button("Delete Student"):
        delete_student(student_id)
        st.success("Student deleted")

# ---------------- ANALYSIS ----------------
elif menu == "Analysis":
    df = fetch_data()

    if df.empty:
        st.warning("No data available")
    else:
        df["Result"] = df["marks"].apply(lambda x: "Pass" if x >= 40 else "Fail")

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Marks", round(df["marks"].mean(), 2))
        col2.metric("Pass Percentage", round((df["Result"] == "Pass").mean() * 100, 2))
        col3.metric("Top Scorer", df.loc[df["marks"].idxmax()]["name"])

        st.subheader("📊 Subject vs Average Marks")
        subject_avg = df.groupby("subject")["marks"].mean()
        st.bar_chart(subject_avg)

        st.subheader("🥧 Pass / Fail Ratio")
        fig, ax = plt.subplots()
        df["Result"].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
        st.pyplot(fig)
