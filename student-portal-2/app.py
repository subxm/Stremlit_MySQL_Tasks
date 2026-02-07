import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# ================== DB CONFIG ==================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "shubham",   # 🔴 CHANGE THIS
    "database": "student_portal"
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor(dictionary=True)

# ================== SESSION ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================== LOGIN ==================
if not st.session_state.logged_in:
    st.title("Student Portal Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    st.stop()

# ================== HELPERS ==================
def get_students():
    cursor.execute("SELECT * FROM students")
    return pd.DataFrame(cursor.fetchall())

# ================== SIDEBAR ==================
st.sidebar.title("Menu")
menu = st.sidebar.selectbox(
    "Select Option",
    ["Add Student", "Mark Attendance", "Add Marks", "Attendance History", "Reports"]
)

# ================== ADD STUDENT ==================
if menu == "Add Student":
    st.header("Add Student")

    with st.form("add_student"):
        roll = st.text_input("Roll No")
        name = st.text_input("Name")
        class_ = st.selectbox("Class", ["A", "B", "C"])
        submit = st.form_submit_button("Add Student")

        if submit:
            try:
                cursor.execute(
                    "INSERT INTO students (roll_no, name, class) VALUES (%s,%s,%s)",
                    (roll, name, class_)
                )
                conn.commit()
                st.success("Student Added Successfully")
            except:
                st.error("Roll No already exists")

# ================== MARK ATTENDANCE ==================
elif menu == "Mark Attendance":
    st.header("Mark Attendance")

    students = get_students()

    if students.empty:
        st.error("No students found")
    else:
        students["label"] = students["name"] + " (" + students["roll_no"] + ")"

        student = st.selectbox("Student", students["label"])
        status = st.radio("Status", ["Present", "Absent"])

        if st.button("Submit Attendance"):
            sid = int(students.loc[students["label"] == student, "id"].values[0])

            cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (%s,%s,%s)",
                (sid, date.today(), status)
            )
            conn.commit()
            st.success("Attendance Recorded")


# ================== ADD MARKS ==================
elif menu == "Add Marks":
    st.header("Add Marks")

    students = get_students()

    if students.empty:
        st.error("No students found")
    else:
        students["label"] = students["name"] + " (" + students["roll_no"] + ")"

        student = st.selectbox("Student", students["label"])
        subject = st.selectbox("Subject", ["Maths", "Physics", "Chemistry"])
        marks = st.number_input("Marks", 0, 100)

        if st.button("Add Marks"):
            sid = int(students.loc[students["label"] == student, "id"].values[0])
            marks = int(marks)

            cursor.execute(
                "INSERT INTO marks (student_id, subject, marks) VALUES (%s,%s,%s)",
                (sid, subject, marks)
            )
            conn.commit()
            st.success("Marks Added Successfully")


# ================== ATTENDANCE HISTORY ==================
elif menu == "Attendance History":
    st.header("Attendance History")

    cursor.execute("""
        SELECT s.name, s.roll_no, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.date DESC
    """)
    df = pd.DataFrame(cursor.fetchall())

    st.dataframe(df)

# ================== REPORTS ==================
elif menu == "Reports":
    st.header("Student Reports")

    students = get_students()

    for _, s in students.iterrows():
        st.subheader(f"{s['name']} ({s['roll_no']})")

        # Attendance %
        cursor.execute(
            "SELECT status FROM attendance WHERE student_id=%s",
            (s["id"],)
        )
        att = pd.DataFrame(cursor.fetchall())

        if not att.empty:
            percent = round((att["status"] == "Present").mean() * 100, 2)
            st.write("Attendance %:", percent)
        else:
            st.write("Attendance %: N/A")

        # Marks + Result
        cursor.execute(
            "SELECT subject, marks FROM marks WHERE student_id=%s",
            (s["id"],)
        )
        marks = pd.DataFrame(cursor.fetchall())

        if not marks.empty:
            st.dataframe(marks)
            result = "Pass" if marks["marks"].mean() >= 40 else "Fail"
            st.write("Result:", result)
        else:
            st.write("No marks available")

        st.divider()
