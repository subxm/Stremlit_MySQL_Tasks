import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="shubham",
        database="student_db"
    )
    print("✅ Database connected successfully")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
