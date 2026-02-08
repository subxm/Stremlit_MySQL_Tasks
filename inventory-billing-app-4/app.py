import streamlit as st
from db import get_connection
from datetime import date

st.set_page_config(page_title="Inventory Management", layout="centered")
st.title("📦 Inventory Management System")

conn = get_connection()
cursor = conn.cursor()

# ➕ Add Product
st.subheader("➕ Add Product")

name = st.text_input("Product Name")
price = st.number_input("Price", min_value=0.0)
stock = st.number_input("Stock", min_value=0, step=1)

if st.button("Add Product"):
    if name:
        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock)
        )
        conn.commit()
        st.success("Product added successfully")

# 📋 View Inventory
st.subheader("📋 Current Inventory")
cursor.execute("SELECT id, name, price, stock FROM products")
products = cursor.fetchall()
st.table(products)

# 📊 Daily Sales Summary
st.subheader("📊 Today's Sales")

cursor.execute(
    "SELECT IFNULL(SUM(total_amount), 0) FROM bills WHERE bill_date=%s",
    (date.today(),)
)
total_sales = cursor.fetchone()[0]

st.metric("Total Sales Today", f"₹ {total_sales}")

conn.close()
