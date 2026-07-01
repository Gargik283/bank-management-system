import streamlit as st
import pandas as pd

from main import BankSystem, Account

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)

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
    st.session_state.page = "Home"


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
st.title("🏦 Bank Management System")
st.caption("Python • PostgreSQL • Streamlit")


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("Navigation")

    if not st.session_state.logged_in:

        choice = st.radio(
            "Menu",
            [
                "Home",
                "Create Account",
                "Login",
                "Admin"
            ]
        )

    else:

        choice = st.radio(
            "Menu",
            [
                "Dashboard",
                "Deposit",
                "Withdraw",
                "Transaction History",
                "Update Account",
                "Delete Account",
                "Logout"
            ]
        )


# ===================================================
# HOME
# ===================================================
if choice == "Home":

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

- Create Account
- Secure Login
- Deposit
- Withdraw
- Balance Check
- Transaction History
- Update Account
- Delete Account
- Admin Audit Logs
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
elif choice == "Create Account":

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

            account = bank.create_account(
                name,
                pin
            )

            if account:

                st.success("Account Created Successfully")

                st.info(
                    f"Account Number : {account.get_account_number()}"
                )

                st.warning(
                    "Save this Account Number safely."
                )

            else:

                st.error(
                    "Unable to create account."
                )


# ===================================================
# LOGIN
# ===================================================
elif choice == "Login":

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
            "Login"
        )

    if login:

        account = Account.load_from_db(
            account_number,
            pin
        )

        if account:

            st.session_state.logged_in = True
            st.session_state.account = account
            st.session_state.pin = pin

            st.success("Login Successful")

            st.rerun()

        else:

            st.error(
                "Invalid Account Number or PIN."
            )

# ===================================================
# DASHBOARD
# ===================================================
elif choice == "Dashboard":

    refresh_account()
    account = st.session_state.account

    st.subheader("Customer Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Account Holder",
            account.get_name()
        )

        st.metric(
            "Account Number",
            account.get_account_number()
        )

    with col2:
        st.metric(
            "Available Balance",
            f"${account.get_balance():,.2f}"
        )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("Use the sidebar to Deposit money.")

    with c2:
        st.info("Use the sidebar to Withdraw money.")

    with c3:
        st.info("View transaction history anytime.")


# ===================================================
# DEPOSIT
# ===================================================
elif choice == "Deposit":

    refresh_account()
    account = st.session_state.account

    st.subheader("Deposit Money")

    st.write(
        f"Current Balance : **${account.get_balance():,.2f}**"
    )

    with st.form("deposit_form"):

        amount = st.number_input(
            "Deposit Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        deposit_btn = st.form_submit_button(
            "Deposit"
        )

    if deposit_btn:

        if amount <= 0:
            st.error("Enter a valid amount.")

        else:

            success = bank.deposit(
                account.get_account_number(),
                st.session_state.pin,
                amount
            )

            if success:

                refresh_account()

                st.success(
                    f"${amount:,.2f} deposited successfully."
                )

                st.metric(
                    "Updated Balance",
                    f"${st.session_state.account.get_balance():,.2f}"
                )

            else:

                st.error(
                    "Deposit failed."
                )


# ===================================================
# WITHDRAW
# ===================================================
elif choice == "Withdraw":

    refresh_account()
    account = st.session_state.account

    st.subheader("Withdraw Money")

    st.write(
        f"Current Balance : **${account.get_balance():,.2f}**"
    )

    with st.form("withdraw_form"):

        amount = st.number_input(
            "Withdraw Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        withdraw_btn = st.form_submit_button(
            "Withdraw"
        )

    if withdraw_btn:

        if amount <= 0:

            st.error("Enter a valid amount.")

        else:

            success = bank.withdraw(
                account.get_account_number(),
                st.session_state.pin,
                amount
            )

            if success:

                refresh_account()

                st.success(
                    f"${amount:,.2f} withdrawn successfully."
                )

                st.metric(
                    "Updated Balance",
                    f"${st.session_state.account.get_balance():,.2f}"
                )

            else:

                st.error(
                    "Withdrawal failed.\n\nPossible reasons:\n- Insufficient balance\n- Invalid amount"
                )

# ===================================================
# TRANSACTION HISTORY
# ===================================================
elif choice == "Transaction History":

    refresh_account()
    account = st.session_state.account

    st.subheader("Transaction History")

    logs = bank.get_audit_logs(account.get_account_number())

    if not logs:
        st.info("No transactions found.")
    else:
        df = pd.DataFrame(logs)
        st.dataframe(df, use_container_width=True)


# ===================================================
# UPDATE ACCOUNT
# ===================================================
elif choice == "Update Account":

    refresh_account()
    account = st.session_state.account

    st.subheader("Update Account")

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


# ===================================================
# DELETE ACCOUNT
# ===================================================
elif choice == "Delete Account":

    refresh_account()
    account = st.session_state.account

    st.subheader("Delete Account")

    st.warning("⚠ This action is permanent and cannot be undone.")

    confirm = st.text_input("Type DELETE to confirm")

    pin = st.text_input("Enter PIN", type="password")

    if st.button("Delete Account"):

        if confirm != "DELETE":
            st.error("Confirmation text does not match.")

        elif pin != st.session_state.pin:
            st.error("Incorrect PIN.")

        else:

            success = account.delete_from_db()

            if success:

                st.success("Account deleted successfully.")

                logout()


# ===================================================
# LOGOUT
# ===================================================
elif choice == "Logout":

    logout()


# ===================================================
# ADMIN PANEL
# ===================================================
elif choice == "Admin":

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
                else:
                    st.error("Failed to clear logs.")

            else:
                st.error("Confirmation failed.")