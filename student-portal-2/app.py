import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Student Attendance & Marks Portal", layout="wide")

# =========================
# MYSQL CONNECTION (SAFE)
# =========================
conn = None
cursor = None
db_connected = True

try:
    conn = mysql.connector.connect(
        host="localhost",          # works locally
        user="root",
        password="YOUR_PASSWORD",  # 🔴 CHANGE THIS
        database="student_portal"
    )
    cursor = conn.cursor(dictionary=True)
except:
    db_connected = False

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN
# =========================
if not st.session_state.logged_in:
    st.title("Student Portal Login")

    with st.form("login"):
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

# =========================
# DEMO MODE WARNING
# =========================
if not db_connected:
    st.warning(
        "⚠️ Database not connected.\n\n"
        "This deployed version is for **UI / demo purposes only**.\n"
        "Full functionality works in **local execution with MySQL**."
    )

# =========================
# HELPER
# =========================
def get_students():
    if not db_connected:
        return pd.DataFrame(columns=["id", "roll_no", "name", "class"])
    cursor.execute("SELECT * FROM students")
    return pd.DataFrame(cursor.fetchall())

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Student", "Mark Attendance", "Add Marks", "Attendance History", "Reports"]
)

# =========================
# ADD STUDENT
# =========================
if menu == "Add Student":
    st.header("Add Student")

    with st.form("add_student"):
        roll = st.text_input("Roll No")
        name = st.text_input("Name")
        class_ = st.selectbox("Class", ["A", "B", "C"])
        submit = st.form_submit_button("Add Student")

        if submit:
            if not db_connected:
                st.error("Database not available in deployed version.")
            else:
                try:
                    cursor.execute(
                        "INSERT INTO students (roll_no, name, class) VALUES (%s,%s,%s)",
                        (roll, name, class_)
                    )
                    conn.commit()
                    st.success("Student Added")
                except:
                    st.error("Roll No already exists")

# =========================
# MARK ATTENDANCE
# =========================
elif menu == "Mark Attendance":
    st.header("Mark Attendance")

    students = get_students()

    if students.empty:
        st.info("No student data available.")
    else:
        students["label"] = students["name"] + " (" + students["roll_no"] + ")"
        student = st.selectbox("Student", students["label"])
        status = st.radio("Status", ["Present", "Absent"])

        if st.button("Submit Attendance"):
            if not db_connected:
                st.error("Attendance feature disabled in deployed version.")
            else:
                sid = int(students.loc[students["label"] == student, "id"].values[0])

                cursor.execute(
                    "INSERT INTO attendance (student_id, date, status) VALUES (%s,%s,%s)",
                    (sid, date.today(), status)
                )
                conn.commit()
                st.success("Attendance Recorded")

# =========================
# ADD MARKS
# =========================
elif menu == "Add Marks":
    st.header("Add Marks")

    students = get_students()

    if students.empty:
        st.info("No student data available.")
    else:
        students["label"] = students["name"] + " (" + students["roll_no"] + ")"
        student = st.selectbox("Student", students["label"])
        subject = st.selectbox("Subject", ["Maths", "Physics", "Chemistry"])
        marks = st.number_input("Marks", 0, 100)

        if st.button("Add Marks"):
            if not db_connected:
                st.error("Marks feature disabled in deployed version.")
            else:
                sid = int(students.loc[students["label"] == student, "id"].values[0])
                marks = int(marks)

                cursor.execute(
                    "INSERT INTO marks (student_id, subject, marks) VALUES (%s,%s,%s)",
                    (sid, subject, marks)
                )
                conn.commit()
                st.success("Marks Added")

# =========================
# ATTENDANCE HISTORY
# =========================
elif menu == "Attendance History":
    st.header("Attendance History")

    if not db_connected:
        st.info("Attendance history unavailable in deployed version.")
    else:
        cursor.execute("""
            SELECT s.name, s.roll_no, a.date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            ORDER BY a.date DESC
        """)
        df = pd.DataFrame(cursor.fetchall())
        st.dataframe(df)

# =========================
# REPORTS
# =========================
elif menu == "Reports":
    st.header("Student Reports")

    if not db_connected:
        st.info("Reports unavailable in deployed version.")
    else:
        students = get_students()

        for _, s in students.iterrows():
            st.subheader(f"{s['name']} ({s['roll_no']})")

            cursor.execute(
                "SELECT status FROM attendance WHERE student_id=%s",
                (int(s["id"]),)
            )
            att = pd.DataFrame(cursor.fetchall())

            if not att.empty:
                percent = round((att["status"] == "Present").mean() * 100, 2)
                st.write("Attendance %:", percent)
            else:
                st.write("Attendance %: N/A")

            cursor.execute(
                "SELECT subject, marks FROM marks WHERE student_id=%s",
                (int(s["id"]),)
            )
            marks_df = pd.DataFrame(cursor.fetchall())

            if not marks_df.empty:
                st.dataframe(marks_df)
                result = "Pass" if marks_df["marks"].mean() >= 40 else "Fail"
                st.write("Result:", result)
            else:
                st.write("No marks available")

            st.divider()
