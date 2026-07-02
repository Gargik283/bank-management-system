import streamlit as st
import pandas as pd
import plotly.express as px

from main import BankSystem, Account
from datetime import datetime, timedelta

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="🏦 Bank Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

/* ---------- Main ---------- */

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1400px;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    background:#f8fafc;
}

/* ---------- Metric Cards ---------- */

div[data-testid="stMetric"]{

    background:white;

    border-radius:18px;

    border:1px solid #e5e7eb;

    padding:18px;

    box-shadow:0 3px 10px rgba(0,0,0,.05);
}

/* ---------- Buttons ---------- */

.stButton>button{

    width:100%;

    border-radius:12px;

    height:3rem;

    font-weight:600;

}

/* ---------- Dataframes ---------- */

[data-testid="stDataFrame"]{

    border-radius:12px;

}

/* ---------- Plotly ---------- */

.js-plotly-plot{

    border-radius:18px;

}

/* ---------- Headers ---------- */

h1,h2,h3{

    color:#0f172a;

}

</style>
""",unsafe_allow_html=True)

bank = BankSystem()

# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

if "pin" not in st.session_state:
    st.session_state.pin = ""

if "page" not in st.session_state:
    st.session_state.page = " 🏠 Home"


# -----------------------------
# FUNCTIONS
# -----------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.account = None
    st.session_state.pin = ""
    st.success("Logged out successfully.")
    st.rerun()


def refresh_account():
    if st.session_state.account:
        acc = Account.load_from_db(
            st.session_state.account.get_account_number(),
            st.session_state.pin
        )
        st.session_state.account = acc


# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
# 🏦 Bank Management System

### Secure Banking • PostgreSQL • Streamlit Dashboard

---
""")
st.caption("Python • PostgreSQL • Streamlit")


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.image(
        "https://img.icons8.com/color/96/bank-building.png",
        width=80
    )

    st.title("🏦 Bank Portal")

    st.caption("Python • PostgreSQL • Streamlit")

    st.markdown("---")

    if not st.session_state.logged_in:

        choice = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "👤 Create Account",
                "🔑 Login",
                "🛠️ Admin"
            ]
        )

    else:

        choice = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "💰 Deposit",
                "💸 Withdraw",
                "📜 Transaction History",
                "📈 Analytics",
                "✏️ Update Account",
                "🗑️ Delete Account",
                "🚪 Logout"
            ]
        )


# ===================================================
# HOME
# ===================================================
if choice == "🏠 Home":

    col1, col2 = st.columns([2, 1])

    with col1:

        st.subheader("Welcome")

        st.write("""
This Bank Management System is developed using:

- Python
- PostgreSQL
- Object Oriented Programming
- SHA-256 PIN Encryption
- Streamlit

Features:

-  👤 Create Account
-  🔑 Secure Login
-  💰 Deposit
-  💸 Withdraw
-  🕒 Balance Check
-  📜 Transaction History
-  🖋️ Update Account
-  🗑️ Delete Account
-  🛠️ Admin Audit Logs
        """)

    with col2:

        st.metric(
            "Database",
            "PostgreSQL"
        )

        st.metric(
            "Backend",
            "Python"
        )

        st.metric(
            "Frontend",
            "Streamlit"
        )


# ===================================================
# CREATE ACCOUNT
# ===================================================
elif choice == "👤 Create Account":

    st.subheader("Create New Account")

    with st.form("create_account"):

        name = st.text_input("Full Name")

        pin = st.text_input(
            "4 Digit PIN",
            type="password"
        )

        confirm = st.text_input(
            "Confirm PIN",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account"
        )

    if submitted:

        if name.strip() == "":
            st.error("Name cannot be empty.")

        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be exactly 4 digits.")

        elif pin != confirm:
            st.error("PIN does not match.")

        else:
            with st.spinner("Creating account..."):
                account = bank.create_account(name,pin)   

            if account:
                st.success("Account Created Successfully")
                st.toast("🎉 Welcome to our bank!")
                st.balloons()
                st.info(f"Account Number : {account.get_account_number()}")
                st.warning("Save this Account Number safely.")

            else:
                st.error("Unable to create account.")


# ===================================================
# LOGIN
# ===================================================
elif choice == "🔑 Login":

    st.subheader("Customer Login")

    with st.form("login"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password"
        )

        login = st.form_submit_button(
            " 🔑 Login"
        )

    if login:
        with st.spinner("Authenticating..."):
            account = Account.load_from_db(account_number,pin)

        if account:
            st.session_state.logged_in = True
            st.session_state.account = account
            st.session_state.pin = pin
            st.success("Login Successful")
            st.toast("👋 Login Successful!")

            st.rerun()

        else:
            st.error("Invalid Account Number or PIN.")
# ===================================================
# DASHBOARD
# ===================================================
elif choice == "📊 Dashboard":

    with st.spinner("Loading dashboard..."):
        refresh_account()
    account = st.session_state.account

    st.title("🏦 Customer Dashboard")
    st.markdown(f"""### 👋 Welcome back, **{account.get_name()}**
    Manage your account, view transactions and monitor your balance securely.
    """)
    st.divider()
    # ==========================
    # Customer Information
    # ==========================
    col1, col2 = st.columns(2)

    with col1:
        st.metric("👤 Account Holder", account.get_name())
        st.metric("🏦 Account Number", account.get_account_number())

    with col2:
        st.metric("💰 Available Balance", f"₹{account.get_balance():,.2f}")
    st.divider()

    # ==========================
    # Quick Actions
    # ==========================

    st.subheader("⚡ Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("💰 Deposit Money")
    with c2:
        st.info("💸 Withdraw Money")
    with c3:
        st.info("📜 Transaction History")

    st.divider()

    # ==========================
    # Recent Transactions
    # ==========================

    st.markdown("## 🕒 Recent Transactions")

    logs = bank.get_recent_transactions(account.get_account_number())

    if logs:

        recent_df = pd.DataFrame(logs)

        recent_df = recent_df.rename(columns={
            "holder_name": "Customer",
            "action": "Action",
            "amount": "Amount",
            "timestamp": "Date & Time"
        })

        st.dataframe(recent_df.head(5), use_container_width=True)

    else:
        st.info("No recent transactions available.")
# ===================================================
# DEPOSIT
# ===================================================
elif choice == "💰 Deposit":

    refresh_account()
    account = st.session_state.account

    st.subheader("Deposit Money")
    st.write(f"Current Balance : **₹{account.get_balance():,.2f}**")

    with st.form("deposit_form"):
        amount = st.number_input(
            "Deposit Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        deposit_btn = st.form_submit_button(" 💰 Deposit")

    if deposit_btn:
        if amount <= 0:
            st.error("Enter a valid amount.")
        else:
            with st.spinner("Processing Deposit..."):
                success = bank.deposit(
                    account.get_account_number(),
                    st.session_state.pin,
                    amount
                )

            if success:

                refresh_account()

                st.success(f"₹{amount:,.2f} deposited successfully.")
                st.toast("💰 Deposit Successful!")
                st.metric("Updated Balance",
                    f"₹{st.session_state.account.get_balance():,.2f}")

            else:
                st.error("Please verify the amount and try again.")


# ===================================================
# WITHDRAW
# ===================================================
elif choice == "💸 Withdraw":

    refresh_account()
    account = st.session_state.account

    st.subheader("Withdraw Money")

    st.write(f"Current Balance : **₹{account.get_balance():,.2f}**")

    with st.form("withdraw_form"):

        amount = st.number_input(
            "Withdraw Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        withdraw_btn = st.form_submit_button(" 💸 Withdraw")

    if withdraw_btn:

        if amount <= 0:
            st.error("Enter a valid amount.")

        else:
            with st.spinner("Processing Withdrawal..."):
                success = bank.withdraw(
                account.get_account_number(),
                st.session_state.pin,
                amount
            )

            if success:

                refresh_account()

                st.success(f"₹{amount:,.2f} withdrawn successfully.")
                st.toast("💸 Withdrawal Successful!")
                st.metric("Updated Balance",f"₹{st.session_state.account.get_balance():,.2f}")

            else:

                st.error("Withdrawal failed.\n\nPossible reasons:\n- Insufficient balance\n- Invalid amount")

# ===================================================
# TRANSACTION HISTORY
# ===================================================
elif choice == "📜 Transaction History":

    refresh_account()
    account = st.session_state.account

    st.subheader("Transaction History")

    logs = bank.get_audit_logs(account.get_account_number())
    transaction_type = st.selectbox(
        "Filter by Transaction Type",
        ["All", " 💰 Deposit", " 💸 Withdraw", " 📄 Account created"]
    )
    minimum_amount = st.number_input(
        "Minimum Amount (₹)",
        min_value=0,
        value=0,
        step=500
    )
    date_filter = st.selectbox(
    "Filter by Date",
    [
        "All",
        "Today",
        "Last 7 Days",
        "Last 30 Days"
    ]
)

    if not logs:
        st.info("No transactions found.")
    else:
        df = pd.DataFrame(
            logs,
            columns=[
                "ID",
                "Account Number",
                "Holder Name",
                "Action",
                "Amount",
                "Date & Time"
            ]
        )
        if transaction_type != "All":
            df = df[df["Action"] == transaction_type]
        if minimum_amount > 0:
            df = df[df["Amount"] >= minimum_amount]

        df["Date & Time"] = pd.to_datetime(df["Date & Time"])

        today = datetime.now()

        if date_filter == "Today":
            df = df[df["Date & Time"].dt.date == today.date()]

        elif date_filter == "Last 7 Days":
            df = df[df["Date & Time"] >= today - timedelta(days=7)]

        elif date_filter == "Last 30 Days":
            df = df[df["Date & Time"] >= today - timedelta(days=30)]

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Transaction History (CSV)",
            data=csv,
            file_name=f"Transaction_History_{account.get_account_number()}.csv",
            mime="text/csv"
        )

# ===================================================
# UPDATE ACCOUNT
# ===================================================
elif choice == "✏️ Update Account":

    refresh_account()
    account = st.session_state.account

    st.subheader("✏️ Update Account")

    option = st.selectbox(
        "Select what you want to update",
        ["Change Name", "Change PIN"]
    )

    if option == "Change Name":

        new_name = st.text_input("New Name")

        if st.button("Update Name"):

            if new_name.strip() == "":
                st.error("Name cannot be empty.")

            else:

                account.set_name(new_name)
                bank.update_account(account)

                refresh_account()

                st.success("Name updated successfully.")
                st.toast("✅ Name Updated")


    elif option == "Change PIN":

        old_pin = st.text_input("Current PIN", type="password")
        new_pin = st.text_input("New PIN", type="password")
        confirm_pin = st.text_input("Confirm New PIN", type="password")

        if st.button("Update PIN"):

            if old_pin != st.session_state.pin:
                st.error("Current PIN is incorrect.")

            elif len(new_pin) != 4 or not new_pin.isdigit():
                st.error("PIN must be 4 digits.")

            elif new_pin != confirm_pin:
                st.error("PIN does not match.")

            else:

                account.set_pin(new_pin)
                bank.update_account(account)

                st.session_state.pin = new_pin
                refresh_account()

                st.success("PIN updated successfully.")
                st.toast("🔐 PIN Updated")


# ===================================================
# DELETE ACCOUNT
# ===================================================
elif choice == "🗑️ Delete Account":

    refresh_account()
    account = st.session_state.account

    st.subheader("🗑️ Delete Account")

    st.warning("⚠ This action is permanent and cannot be undone.")

    confirm = st.text_input("Type DELETE to confirm")

    pin = st.text_input("Enter PIN", type="password")

    if st.button("🗑️ Delete Account"):

        if confirm != "DELETE":
            st.error("Confirmation text does not match.")

        elif pin != st.session_state.pin:
            st.error("Incorrect PIN.")

        else:
            success = account.delete_from_db()

            if success:
                st.success("Account deleted successfully.")
                st.toast("Account Closed Successfully")

                logout()

# ===================================================
# LOGOUT
# ===================================================
elif choice == "🚪 Logout":
    logout()

# ===================================================
# ADMIN PANEL
# ===================================================
elif choice == "🛠️ Admin":
    st.subheader("Admin Panel")

    admin_option = st.selectbox(
        "Select Action",
        [
            "View All Audit Logs",
            "Clear Audit Logs"
        ]
    )

    if admin_option == "View All Audit Logs":

        logs = bank.get_all_audit_logs()

        if not logs:
            st.info("No audit logs available.")
        else:
            df = pd.DataFrame(logs)
            st.dataframe(df, use_container_width=True)


    elif admin_option == "Clear Audit Logs":

        st.warning("This will permanently delete all audit logs.")

        confirm = st.text_input("Type CONFIRM to proceed")

        if st.button("Clear Logs"):

            if confirm == "CONFIRM":

                success = bank.clear_audit_logs()

                if success:
                    st.success("Audit logs cleared successfully.")
                    st.toast("Audit Logs Deleted")
                else:
                    st.error("Failed to clear logs.")

            else:
                st.error("Confirmation failed.")

# ===================================================
# ANALYTICS
# ===================================================
elif choice == "📈 Analytics":

    refresh_account()
    account = st.session_state.account

    st.title("📊 Bank Analytics Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👤 Account Holder",
            account.get_name()
        )
    with col2:
        st.metric(
            "🏦 Account Number",
            account.get_account_number()
        )
    with col3:
        st.metric(
            "💰 Available Balance",
            f"₹{account.get_balance():,.2f}"
        )
    if account.get_balance() >= 50000:
        st.success("🟢 Excellent Balance")

    elif account.get_balance() >= 10000:
        st.info("🔵 Healthy Balance")

    else:
        st.warning("🟠 Low Balance")

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "📥 Total Deposits",
            f"₹{bank.get_total_deposits():,.2f}"
        )

    with col4:
        st.metric(
            "📤 Total Withdrawals",
            f"₹{bank.get_total_withdrawals():,.2f}"
        )

    st.divider()

    chart_data = pd.DataFrame({
        "Transaction": [" 💰 Deposits", " 💸 Withdrawals"],
        "Amount": [
            bank.get_total_deposits(),
            bank.get_total_withdrawals()
        ]
    })

    fig = px.bar(
        chart_data,
        x="Transaction",
        y="Amount",
        text="Amount",
        title="Deposits vs Withdrawals"
    )
    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    st.subheader("🏆 Top 10 Richest Customers")

    top_accounts = bank.get_top_accounts()

    if top_accounts:

        df = pd.DataFrame(
            top_accounts,
            columns=["Customer", "Balance"]
        )

        fig2 = px.bar(
            df,
            x="Balance",
            y="Customer",
            orientation="h",
            text="Balance",
            title="Top 10 Richest Customers",
            color="Balance",
            color_continuous_scale="Greens"
        )
        fig2.update_layout(
            template="plotly_white",
            title_x=0.5,
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.divider()
        st.subheader("📈 Daily Transactions")

        daily_data = bank.get_daily_transactions()

        if daily_data:

            df_daily = pd.DataFrame(
                daily_data,
                columns=["Date", "Transactions"]
            )

            fig3 = px.line(
                df_daily,
                x="Date",
                y="Transactions",
                markers=True,
                title="Daily Transaction Trend"
            )
            fig3.update_layout(
                template="plotly_white",
                title_x=0.5
            )

            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No transaction data available.")

    else:
        st.info("No accounts found.")

    st.success("Analytics Dashboard Loaded Successfully ✅")

    st.markdown("---")

    st.caption(
    "🏦 Bank Management System | Developed by Gargi Kundu | Python • PostgreSQL • Streamlit"
)