import csv
import getpass
from datetime import datetime

class BankAccount:
    """Class representing a bank account."""

    def __init__(self, acc_num, password, balance=0):
        """Initialize the BankAccount object."""
        self.acc_num = acc_num
        self.password = password
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        """Deposit funds into the account."""
        self.balance += amount
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transactions.append(
            f"{timestamp}: Deposited ₹{amount}. Current balance: ₹{self.balance}")
        return f"Deposited ₹{amount}. Current balance: ₹{self.balance}"

    def withdraw(self, amount, password=None):
        """Withdraw funds from the account."""
        if password is not None and not self.verify_password(password):
            return "Incorrect password. Withdrawal denied."

        if amount <= self.balance:
            self.balance -= amount
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.transactions.append(
                f"{timestamp}: Withdrew ₹{amount}. Current balance: ₹{self.balance}")
            return f"Withdrew ₹{amount}. Current balance: ₹{self.balance}"
        else:
            return "Insufficient funds!"

    def get_balance(self):
        """Get the current balance of the account."""
        return f"Account balance for account {self.acc_num}: ₹{self.balance}"

    def get_transaction_history(self):
        """Get the transaction history of the account."""
        history = []
        for transaction in self.transactions:
            timestamp, description = transaction.split(': ', 1)
            history.append((datetime.strptime(timestamp,
                                                '%Y-%m-%d %H:%M:%S'), description))
        return history

    def verify_password(self, password):
        """Verify the account password."""
        return self.password == password

    def to_list(self):
        """Convert account information to a list."""
        return [self.acc_num, self.password, self.balance]

    @classmethod
    def from_list(cls, data):
        """Create a BankAccount object from a list of data."""
        try:
            return cls(data[0], data[1], float(data[2]))
        except (ValueError, IndexError) as e:
            print(f"Error creating BankAccount from data: {e}")
            return None

    @classmethod
    def find_account(cls, accounts, acc_num):
        """Find an account by account number."""
        for acc in accounts:
            if acc.acc_num == acc_num:
                return acc
        return None

    @classmethod
    def account_exists(cls, accounts, acc_num):
        """Check if an account exists."""
        return any(acc.acc_num == acc_num for acc in accounts)


def save_accounts_csv(accounts, filename="accounts.csv"):
    """Save account information to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Account Number", "Password", "Balance"])
        for account in accounts:
            writer.writerow(account.to_list())


def save_transaction_history_csv(account, filename="transaction_history.csv"):
    """Save transaction history to a CSV file."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for transaction in account.get_transaction_history():
            timestamp, description = transaction
            writer.writerow([
                account.acc_num,
                timestamp.strftime('%Y-%m-%d %H:%M:%S'), description
            ])


def load_accounts_csv(filename="accounts.csv",
                      history_filename="transaction_history.csv"):
    """Load account information from a CSV file."""
    try:
        with open(filename, "r", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            valid_accounts = [BankAccount.from_list(row) for row in reader]

        try:
            with open(history_filename, "r", newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    acc_num, timestamp, description = row
                    datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    account = BankAccount.find_account(valid_accounts, acc_num)
                    if account:
                        account.transactions.append(f"{timestamp}: {description}")

        except FileNotFoundError:
            pass

        return valid_accounts

    except FileNotFoundError:
        return []
