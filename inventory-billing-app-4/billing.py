import streamlit as st
from db import get_connection
from datetime import date
import pandas as pd

st.set_page_config(page_title="Billing System", layout="wide")
st.title("🧾 Billing System")

conn = get_connection()
cursor = conn.cursor()

# Cart using session state
if "cart" not in st.session_state:
    st.session_state.cart = []

# Fetch products
cursor.execute("SELECT id, name, price, stock FROM products")
products = cursor.fetchall()

st.subheader("🛒 Add Products")

for p in products:
    col1, col2, col3, col4 = st.columns(4)
    col1.write(p[1])
    col2.write(f"₹{p[2]}")
    qty = col3.number_input("Qty", 0, p[3], key=p[0])

    if col4.button("Add", key=f"add{p[0]}"):
        if qty > 0:
            st.session_state.cart.append((p[0], p[1], p[2], qty))

# 🧾 Cart Display
st.subheader("🧾 Cart")

total = 0
for item in st.session_state.cart:
    st.write(f"{item[1]} × {item[3]}")
    total += item[2] * item[3]

st.metric("Total Amount", f"₹ {total}")

# 🧾 Generate Bill
if st.button("Generate Bill") and total > 0:
    cursor.execute(
        "INSERT INTO bills (bill_date, total_amount) VALUES (%s, %s)",
        (date.today(), total)
    )
    bill_id = cursor.lastrowid

    for item in st.session_state.cart:
        cursor.execute(
            "INSERT INTO bill_items (bill_id, product_id, quantity) VALUES (%s, %s, %s)",
            (bill_id, item[0], item[3])
        )
        cursor.execute(
            "UPDATE products SET stock = stock - %s WHERE id = %s",
            (item[3], item[0])
        )

    conn.commit()
    st.success("✅ Bill Generated Successfully")

    df = pd.DataFrame(
        st.session_state.cart,
        columns=["Product ID", "Product Name", "Price", "Quantity"]
    )

    st.download_button(
        "⬇ Download Bill",
        df.to_csv(index=False),
        file_name="bill.csv"
    )

    st.session_state.cart = []

conn.close()
