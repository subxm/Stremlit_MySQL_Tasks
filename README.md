# 🚀 Streamlit MySQL Tasks – Full Project Repository

This repository contains multiple **Streamlit-based applications** developed as part of database-integrated web application tasks.  
Each task focuses on solving a **real-world problem** using **Streamlit + Python + Database (MySQL/SQLite)**.

---

## 📂 Repository Structure



## ✅ TASK 1: Student Performance Management System

📁 Folder: `student-performance-1/`

### Description
A system to manage and analyze student academic performance.

### Key Features
- Add student records
- Store marks and grades
- View student performance
- Database-backed storage

### Concepts Used
- Streamlit forms
- Database CRUD operations
- Data display using tables

---

## ✅ TASK 2: Student Portal System

📁 Folder: `student-portal-2/`

### Description
A basic student portal to manage student information and interactions.

### Key Features
- Student data entry
- Viewing stored student details
- Structured backend logic

### Concepts Used
- Streamlit UI components
- Modular Python code
- Database connectivity

---

## ✅ TASK 3: Online Complaint Management System

📁 Folder: `complaint-management-3/`

### Description
An online complaint registration and tracking system with **User** and **Admin** roles.

### Key Features
- User complaint submission
- Auto-generated complaint ID
- Admin dashboard to:
  - View complaints
  - Update complaint status
  - Search complaints by ID
- Input validation
- Status tracking (Open / In Progress / Closed)

### Streamlit Concepts Used
- `st.text_area()`
- `st.selectbox()`
- `st.expander()`
- `st.sidebar()`
- `st.session_state`
- Database integration (MySQL)

---

## ✅ TASK 4: Inventory & Billing Management App

📁 Folder: `inventory-billing-app-4/`

### Description
A shop inventory and billing system that manages products, generates bills, and tracks sales.

### Key Features
- Add products (Name, Price, Stock)
- Billing system with cart handling
- Auto stock update after purchase
- Store bills and bill items in database
- Daily sales summary
- Download bill as CSV

### Streamlit Concepts Used
- `st.number_input()`
- `st.columns()`
- `st.metric()`
- `st.download_button()`
- `st.session_state` for cart handling

### Database Tables
- `products`
- `bills`
- `bill_items`

---

## 🧰 Tech Stack Used Across Tasks

- **Frontend & Backend**: Streamlit
- **Programming Language**: Python
- **Database**: MySQL (Local)
- **Version Control**: Git & GitHub

---

## ☁️ Deployment Notes (Important)

- Applications are deployed on **Streamlit Community Cloud**
- Local MySQL databases are **not accessible in cloud environments**
- Database connection errors in deployment are **expected and explained**
- Code logic and structure remain correct and production-ready

---

## 🎯 Learning Outcomes

- Real-world Streamlit application development
- Database schema design & normalization
- CRUD operations with MySQL
- Session management and state handling
- Modular project structure
- Git & GitHub workflow
- Cloud deployment understanding

---

