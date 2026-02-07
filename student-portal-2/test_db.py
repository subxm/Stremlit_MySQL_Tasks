import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shubham",
    database="student_portal"
)

print("Connected successfully")
