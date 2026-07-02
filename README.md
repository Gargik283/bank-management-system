# 🏦 Bank Management System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Analytics-3F4F75?style=for-the-badge&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

<p align="center">

### 🚀 A Secure Banking Management System built using Python, PostgreSQL & Streamlit

Manage bank accounts, perform transactions, visualize analytics, and maintain audit logs through an interactive dashboard.

🌐 **Live Demo:** https://gargik283-bank-management-system-app-gkw546.streamlit.app/

</p>

---

# 📌 Table of Contents

- Project Overview
- Features
- Tech Stack
- Screenshots
- Project Structure
- Database Design
- Installation
- Running the Application
- Analytics Dashboard
- Future Improvements
- Author

---

# 📖 Project Overview

The **Bank Management System** is a full-stack banking application developed using **Python**, **PostgreSQL**, and **Streamlit**.

It demonstrates secure banking operations while following Object-Oriented Programming principles and relational database design.

The application allows users to:

- Create bank accounts
- Login securely
- Deposit money
- Withdraw money
- Update account information
- Delete accounts
- View transaction history
- Download transaction history as CSV
- Analyze banking data through interactive dashboards
- Track every activity using audit logs

---

# ✨ Features

## 👤 Customer Module

- Create New Account
- Secure Login
- Deposit Money
- Withdraw Money
- View Balance
- Update Name
- Update PIN
- Delete Account
- Recent Transactions
- Download Transaction History (CSV)

---

## 📊 Analytics Dashboard

- Deposit vs Withdrawal Analysis
- Daily Transaction Trend
- Top 10 Richest Customers
- Balance Health Indicator
- Interactive Plotly Charts

---

## 🛡️ Security

- SHA-256 PIN Hashing
- Parameterized SQL Queries
- Session-Based Authentication
- PostgreSQL Database

---

## 🛠️ Admin Features

- View Audit Logs
- Clear Audit Logs
- Monitor User Activity

---

# 💻 Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend Logic |
| PostgreSQL | Database |
| Streamlit | Web Interface |
| Plotly | Data Visualization |
| Pandas | Data Processing |
| psycopg2 | PostgreSQL Connectivity |
| hashlib | PIN Encryption |
| python-dotenv | Environment Variables |

---

# 📸 Application Screenshots

## 🏠 Home

![](screenshots/home.png)

---

## 👤 Create Account

![](screenshots/create.png)

---

## 🔑 Login

![](screenshots/login.png)

---

## 📊 Dashboard

![](screenshots/dashboard.png)

---

## 💰 Deposit

![](screenshots/deposit.png)

---

## 📜 Transaction History

![](screenshots/transaction_history.png)

---

## 📈 Analytics Dashboard

![](screenshots/analytics1.png)

![](screenshots/analytics2.png)

---

# 📂 Project Structure

```
Bank-Management-System
│
├── screenshots/
├── app.py
├── main.py
├── database.py
├── pdf_generator.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

---

# 🗄️ Database

## Accounts Table

- Account Number
- Customer Name
- PIN (SHA-256 Hash)
- Balance
- Created Date

---

## Audit Table

Stores every transaction including:

- Deposit
- Withdraw
- Account Created
- Account Updated
- Timestamp

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Gargik283/bank-management-system.git
```

Move into the project

```bash
cd bank-management-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure Environment Variables

Create a `.env` file in the project root.

```env
DB_HOST=localhost
DB_PORT=2004
DB_NAME=banksystemmanagement
DB_USER=postgres
DB_PASSWORD=your_password
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will launch at:

```
http://localhost:8501
```

---

# 📊 Analytics Included

✔ Deposit Analysis

✔ Withdrawal Analysis

✔ Daily Transaction Trends

✔ Top 10 Richest Customers

✔ Account Balance Monitoring

✔ Audit Log Tracking

---

# 🚀 Future Improvements

- Export Transactions as PDF
- Email Notifications
- OTP Authentication
- Role-Based Access Control
- Password Recovery
- Cloud Database Integration
- Docker Deployment
- AI-powered Fraud Detection
- Power BI Dashboard Integration

---

# 👩‍💻 Author

**Gargi Kundu**

B.Tech Graduate | Python | SQL | PostgreSQL | Streamlit | Data Analytics

GitHub: https://github.com/Gargik283

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and supports future improvements.
