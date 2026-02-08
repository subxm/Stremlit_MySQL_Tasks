import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="shubham",
        database="complaint_db"
    )
    print("✅ MySQL Connected Successfully")
    conn.close()
except mysql.connector.Error as e:
    print("❌ MySQL Connection Failed")
    print(e)
