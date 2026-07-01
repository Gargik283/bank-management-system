import random
import string
import hashlib
import psycopg2
import os
from database import connect_to_database

# ==================== UTILITY FUNCTIONS ====================
def _hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def _verify_pin(input_pin, stored_hash):
    return _hash_pin(input_pin) == stored_hash

def get_valid_amount(prompt):
    while True:
        amount_str = input(prompt).strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

# ==================== DATABASE TABLE INITIALIZATION ====================
def initialize_tables():
    connection = connect_to_database()
    if not connection:
        return False
        
    try:
        cursor = connection.cursor()
        create_accounts_table = """
        CREATE TABLE IF NOT EXISTS accounts (
            account_number VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            pin VARCHAR(64) NOT NULL,
            balance DECIMAL(15, 2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        create_audit_table = """
        CREATE TABLE IF NOT EXISTS audit (
            id SERIAL PRIMARY KEY,
            account_number VARCHAR(20),
            holder_name VARCHAR(100),
            action VARCHAR(100) NOT NULL,
            amount DECIMAL(15,2) DEFAULT 0.00,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_number) 
            REFERENCES accounts(account_number)
            ON DELETE CASCADE
        );
        """
        
        cursor.execute(create_accounts_table)
        cursor.execute(create_audit_table)
        
        connection.commit()
        cursor.close()
        return True
    except Exception as error:
        print(f"Error initializing tables: {error}")
        return False

# ==================== AUDIT CLASS ====================
class Audit:    
    @staticmethod
    def log_action(account_number, holder_name, action, amount = 0.0):
        connection = connect_to_database()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO audit (account_number, holder_name, action, amount) VALUES (%s, %s, %s, %s)",
                (account_number, holder_name, action, amount)
            )
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Error logging audit action: {error}")
            return False
    
    @staticmethod
    def get_audit_logs(account_number):
        connection = connect_to_database()
        if not connection:
            return []
            
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, holder_name, action, amount, timestamp 
                FROM audit 
                WHERE account_number = %s 
                ORDER BY timestamp DESC
                """,
                (account_number,)
            )
            results = cursor.fetchall()
            cursor.close()
            
            logs = []
            for row in results:
                logs.append({
                    'id': row[0],
                    'holder_name': row[1],
                    'action': row[2],
                    'amount': float(row[3]),
                    'timestamp': row[4]
                })
            return logs
        except Exception as error:
            print(f"Error retrieving audit logs: {error}")
            return []
    
    @staticmethod
    def get_all_audit_logs():
        connection = connect_to_database()
        if not connection:
            return []
            
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, account_number, holder_name, action, amount, timestamp 
                FROM audit 
                ORDER BY timestamp DESC
                """
            )
            results = cursor.fetchall()
            cursor.close()
            
            logs = []
            for row in results:
                logs.append({
                    'id': row[0],
                    'account_number': row[1],
                    'holder_name': row[2],
                    'action': row[3],
                    'amount': float(row[4]),
                    'timestamp': row[5]
                })
            return logs
        except Exception as error:
            print(f"Error retrieving all audit logs: {error}")
            return []
    
    @staticmethod
    def clear_audit_logs():
        connection = connect_to_database()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM audit")
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Error clearing audit logs: {error}")
            return False

# ==================== ACCOUNT CLASS ====================
class Account:    
    def __init__(self, name = "", pin = "", account_number = ""):
        self.__account_number = account_number if account_number else self.__generate_account_number()
        self.__name = name
        self.__pin = _hash_pin(pin) if pin else ""
        self.__balance = 0.0
        
    @staticmethod
    def __generate_account_number():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    def get_account_number(self):
        return self.__account_number
    
    def get_name(self):
        return self.__name
    
    def get_balance(self):
        return self.__balance
    
    def get_pin_hash(self):
        return self.__pin
    
    def set_name(self, name):
        self.__name = name
    
    def set_pin(self, pin):
        self.__pin = _hash_pin(pin)
    
    def set_balance(self, balance):
        self.__balance = balance
    
    def deposit(self, amount):
        if amount <= 0:
            return False
        self.__balance += amount
        return True
    
    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True
    
    @classmethod
    def load_from_db(cls, account_number, pin):
        connection = connect_to_database()
        if not connection:
            return None
            
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT account_number, name, pin, balance FROM accounts WHERE account_number = %s",
                (account_number,)
            )
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                stored_pin_hash = result[2]
                if _verify_pin(pin, stored_pin_hash):
                    account = cls(result[1], "", result[0])  
                    account.set_balance(float(result[3]))
                    account.__pin = stored_pin_hash
                    return account
            return None
        except Exception as error:
            print(f"Error loading account: {error}")
            return None
    
    def save_to_db(self):
        connection = connect_to_database()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO accounts (account_number, name, pin, balance)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (account_number)
                DO UPDATE SET name = %s, pin = %s, balance = %s
                """,
                (self.__account_number, self.__name, self.__pin, self.__balance,
                 self.__name, self.__pin, self.__balance)
            )
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Error saving account: {error}")
            return False
    
    def delete_from_db(self):
        connection = connect_to_database()
        if not connection:
            return False
            
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM accounts WHERE account_number = %s", (self.__account_number,))
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Error deleting account: {error}")
            return False

# ==================== BANK SYSTEM CLASS ====================
class BankSystem:
    def __init__(self):
        initialize_tables()

    def _account_exists(self, account_number):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT 1 FROM accounts WHERE account_number = %s",
                (account_number,)
            )
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        except Exception as error:
            print(f"Error checking account existence: {error}")
            return False

    def create_account(self, name, pin):
        account = Account(name, pin)
        while self._account_exists(account.get_account_number()):
            account = Account(name, pin)

        if account.save_to_db():
            Audit.log_action(account.get_account_number(), account.get_name(), "Account created")
            return account
        return None

    def deposit(self, account_number, pin, amount):
        account = Account.load_from_db(account_number, pin)
        if not account:
            return False
        if account.deposit(amount) and account.save_to_db():
            Audit.log_action(account.get_account_number(), account.get_name(), "Deposit", amount)
            return True
        return False

    def withdraw(self, account_number, pin, amount):
        account = Account.load_from_db(account_number, pin)
        if not account:
            return False
        if account.withdraw(amount) and account.save_to_db():
            Audit.log_action(account.get_account_number(), account.get_name(), "Withdraw", amount)
            return True
        return False

    def update_account(self, account):
        if account.save_to_db():
            Audit.log_action(account.get_account_number(), account.get_name(), "Account updated")
            return True
        return False

    def delete_account(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)
        if not account:
            return False
        return account.delete_from_db()

    def get_audit_logs(self, account_number):
        return Audit.get_audit_logs(account_number)

    def get_all_audit_logs(self):
        return Audit.get_all_audit_logs()

    def clear_audit_logs(self):
        return Audit.clear_audit_logs()
    
    def get_total_accounts(self):
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM accounts")
        total = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return total

    def get_total_bank_balance(self):
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("SELECT COALESCE(SUM(balance),0) FROM accounts")
        total = float(cursor.fetchone()[0])

        cursor.close()
        connection.close()

        return total

    def get_total_deposits(self):
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount),0)
            FROM audit
            WHERE action='Deposit'
        """)

        total = float(cursor.fetchone()[0])

        cursor.close()
        connection.close()

        return total

    def get_total_withdrawals(self):
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(amount),0)
            FROM audit
            WHERE action='Withdraw'
        """)

        total = float(cursor.fetchone()[0])

        cursor.close()
        connection.close()

        return total
    
    def get_top_accounts(self):
        connection = connect_to_database()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT name, balance
            FROM accounts
            ORDER BY balance DESC
            LIMIT 10
        """)

        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

# ==================== CLI MENU FUNCTIONS ====================
def create_account_cli(bank):
    print("=" * 40)
    print("        CREATE NEW ACCOUNT")
    print("=" * 40)
    
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        input("Press Enter to continue...")
        return
    
    pin = input("Insert 4-digit PIN: ").strip()
    if len(pin) != 4 or not pin.isdigit():
        print("PIN should be 4-digit number.")
        input("Press Enter to continue...")
        return
    
    confirm_pin = input("Confirm your PIN: ").strip()
    if pin != confirm_pin:
        print("PIN not matching.")
        input("Press Enter to continue...")
        return
    
    account = bank.create_account(name, pin)
    if account:
        print(f"\nAccount created successfully!")
        print(f"Account Number: {account.get_account_number()}")
        print("Save your account number and PIN securely.")
    else:
        print("\nAccount creation failed, please try again.")

    input("Press Enter to continue...")

def login_to_account_cli(bank):
    print("=" * 40)
    print("ACCOUNT LOGIN")
    print("=" * 40)
    
    account_number = input("Enter your account number: ").strip()
    if not account_number:
        print("Account number cannot be empty.")
        input("Press Enter to continue...")
        return
    
    pin = input("Please enter your PIN: ").strip()
    
    account = Account.load_from_db(account_number, pin)
    if not account:
        print("Wrong account number or PIN.")
        input("Press Enter to continue...")
        return
    
    while True:
        account = Account.load_from_db(account_number, pin)
        if not account:
            print("Session expired or account deleted.")
            input("Press Enter to continue...")
            break
        print("=" * 40)
        print(f"        WELCOME, {account.get_name()}!")
        print(f"        ACCOUNT: {account.get_account_number()}")
        print("=" * 40)
        print("1. Check your Balance")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. View transaction history")
        print("5. Update account information")
        print("6. Delete account")
        print("7. Logout")
        print("=" * 40)
        
        choice = input("Enter your choice(1-7): ").strip()
        
        if choice == '1':
            check_balance_cli(bank, account)
        elif choice == '2':
            deposit_money_cli(bank, account, pin)
        elif choice == '3':
            withdraw_money_cli(bank, account, pin)
        elif choice == '4':
            view_transaction_history_cli(bank, account)
        elif choice == '5':
            update_account_info_cli(bank, account)
        elif choice == '6':
            if delete_account_cli(bank, account):
                break  
        elif choice == '7':
            break  
        else:
            print("Wrong choice. Please try again.")
            input("Press Enter to continue...")

def check_balance_cli(bank, account):
    print("=" * 40)
    print("         ACCOUNT BALANCE")
    print("=" * 40)
    print(f"Current Balance: ${account.get_balance():.2f}")
    input("Press Enter to continue...")

def deposit_money_cli(bank, account, pin):
    print("=" * 40)
    print("          Deposit Money")
    print("=" * 40)
    amount = get_valid_amount("Enter the amount to deposit: $")
    if bank.deposit(account.get_account_number(), pin, amount):
        print(f"${amount:.2f} Deposited successfully!")
    else:
        print("An error occurred while depositing money. Please try again.")
    input("Press Enter to continue...")

def withdraw_money_cli(bank, account, pin):
    print("=" * 40)
    print("         Withdraw Money")
    print("=" * 40)
    
    amount = get_valid_amount("Enter the amount to withdraw: $")

    if bank.withdraw(account.get_account_number(), pin, amount):
        print(f"${amount:.2f} Withdrawn successfully!")
        account = Account.load_from_db(account.get_account_number(), pin)
        if account:
            print(f"New Balance: ${account.get_balance():.2f}")
    else:
        print("An error occurred while withdrawing. Insufficient funds or invalid amount.")
    
    input("Press Enter to continue...")

def view_transaction_history_cli(bank, account):
    print("=" * 40)
    print("      TRANSACTION HISTORY")
    print("=" * 40)
    
    logs = bank.get_audit_logs(account.get_account_number())
    if not logs:
        print("No transaction history found.")
    else:
        for log in logs:
            print(f"[{log['timestamp']}] {log['action']} - Amount: ${log['amount']:.2f}")
    input("Press Enter to continue...")

def update_account_info_cli(bank, account):
    print("=" * 40)
    print("      UPDATE ACCOUNT INFO")
    print("=" * 40)
    print("1. Change name")
    print("2. Change PIN")
    print("3. Return to Account Menu")
    print("=" * 40)
    
    choice = input("Enter your choice(1-3): ").strip()
    
    if choice == '1':
        new_name = input("Enter new name: ").strip()
        if new_name:
            account.set_name(new_name)
            if bank.update_account(account):
                print("Name updated successfully!")
            else:
                print(" An error occurred while updating the name.")
        else:
            print("Name cannot be empty.")
    elif choice == '2':
        old_pin = input("Enter Current PIN: ").strip()
        if _verify_pin(old_pin, account.get_pin_hash()):
            new_pin = input("Enter new PIN: ").strip()
            if len(new_pin) == 4 and new_pin.isdigit():
                confirm_pin = input("Confirm New PIN: ").strip()
                if new_pin == confirm_pin:
                    account.set_pin(new_pin)
                    if bank.update_account(account):
                        print("PIN successfully updated!")
                    else:
                        print("PIN update failed. Please try again.")
                else:
                    print("PINs do not match.")
            else:
                print("PIN must be a 4-digit number.")
        else:
            print("Invalid current PIN.")
    elif choice != '3':
        print("Invalid choice.")
    
    input("Press Enter to continue...")

def delete_account_cli(bank, account):
    print("=" * 40)
    print("        DELETE ACCOUNT")
    print("=" * 40)
    print("WARNING: The action cannot be undone!")
    print("To confirm you must provide the following information:")
    print(f"1. Account Number: {account.get_account_number()}")
    print("2. Your PIN")
    print("=" * 40)
    
    confirmation = input("Do you really want to delete your account? (yes/no): ").strip().lower()
    if confirmation != 'yes':
        print("Account deletion cancelled.")
        input("Press Enter to continue...")
        return False
    
    acc_num_input = input("Enter your account number: ").strip()
    pin_input = input("Enter your PIN: ").strip()
    
    if acc_num_input == account.get_account_number() and _verify_pin(pin_input, account.get_pin_hash()):
        if bank.delete_account(account.get_account_number(), pin_input):
            print("Account successfully deleted!")
            input("Press Enter to continue...")
            return True
        else:
            print("An error occurred while deleting the account.")
    else:
        print("Account number or PIN is incorrect. Deletion canceled.")
    
    input("Press Enter to continue...")
    return False

def admin_view_audit_logs_cli(bank):
    print("=" * 40)
    print("       VIEW AUDIT LOGS")
    print("=" * 40)
    
    logs = bank.get_all_audit_logs()
    if not logs:
        print("No audit logs found.")
    else:
        print(f"{'ID':<5} {'Account':<12} {'Name':<15} {'Action':<20} {'Amount':<10} {'Time':<20}")
        print("-" * 85)
        for log in logs:
            amount_str = f"${log['amount']:.2f}" if log['amount'] > 0 else ""
            print(f"{log['id']:<5} {log['account_number']:<12} {log['holder_name']:<15} {log['action']:<20} {amount_str:<10} {log['timestamp']}")
    
    input("Press Enter to continue...")

def admin_clear_audit_logs_cli(bank):
    print("=" * 40)
    print("      CLEAR AUDIT LOGS")
    print("=" * 40)
    print("WARNING: This will permanently delete all audit logs!")
    print("=" * 40)
    
    confirmation = input("Do you really want to clear all audit logs? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        if bank.clear_audit_logs():
            print("All audit logs successfully cleared!")
        else:
            print("An error occurred while clearing the audit logs.")
    else:
        print("Operation cancelled.")
    
    input("Press Enter to continue...")

def main_menu_cli():
    bank = BankSystem()
    
    while True:
        print("=" * 40)
        print("        BANK MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Create New Account")
        print("2. Login to Existing Account")
        print("3. Admin - View All Audit Logs")
        print("4. Admin - Clear Audit Logs")
        print("5. Exit")
        print("=" * 40)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            create_account_cli(bank)
        elif choice == '2':
            login_to_account_cli(bank)
        elif choice == '3':
            admin_view_audit_logs_cli(bank)
        elif choice == '4':
            admin_clear_audit_logs_cli(bank)
        elif choice == '5':
            print("Thank you for using our Bank Management System!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu_cli()