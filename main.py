import csv
import getpass
from datetime import datetime


class BankAccount:

  def __init__(self, acc_num, password, balance=0):
    self.acc_num = acc_num
    self.password = password
    self.balance = balance
    self.transactions = []

  def deposit(self, amount):
    self.balance += amount
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.transactions.append(
        f"{timestamp}: Deposited ₹{amount}. Current balance: ₹{self.balance}")
    return f"Deposited ₹{amount}. Current balance: ₹{self.balance}"

  def withdraw(self, amount, password=None):
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
    return f"Account balance for account {self.acc_num}: ₹{self.balance}"

  def get_transaction_history(self):
    history = []
    for transaction in self.transactions:
      timestamp, description = transaction.split(': ', 1)
      history.append((datetime.strptime(timestamp,
                                        '%Y-%m-%d %H:%M:%S'), description))
    return history

  def verify_password(self, password):
    return self.password == password

  def to_list(self):
    return [self.acc_num, self.password, self.balance]

  @classmethod
  def from_list(cls, data):
    try:
      return cls(data[0], data[1], float(data[2]))
    except (ValueError, IndexError) as e:
      print(f"Error creating BankAccount from data: {e}")
      return None

  @classmethod
  def find_account(cls, accounts, acc_num):
    for acc in accounts:
      if acc.acc_num == acc_num:
        return acc
    return None

  @classmethod
  def account_exists(cls, accounts, acc_num):
    return any(acc.acc_num == acc_num for acc in accounts)


def save_accounts_csv(accounts, filename="accounts.csv"):
  with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Account Number", "Password", "Balance"])
    for account in accounts:
      writer.writerow(account.to_list())


def save_transaction_history_csv(account, filename="transaction_history.csv"):
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
  try:
    with open(filename, "r", newline='') as file:
      reader = csv.reader(file)
      next(reader)  # Skip header row
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


if __name__ == "__main__":
  accounts = load_accounts_csv()

  while True:
    print("\nBanking System Menu:")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. View Transaction History")
    print("6. Exit")
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
      acc_num = input("Enter account number: ")
      password = getpass.getpass("Enter account password: ")
      if BankAccount.account_exists(accounts, acc_num):
        print(
            "Account already exists. Please choose a different account number."
        )
      else:
        accounts.append(BankAccount(acc_num, password))
        save_accounts_csv(accounts)
        print(f"Account {acc_num} created successfully!")

    elif choice == "2":
      acc_num = input("Enter account number: ")
      amount = input("Enter deposit amount: ")
      try:
        amount = float(amount)
        account = BankAccount.find_account(accounts, acc_num)
        if account:
          print(account.deposit(amount))
          save_accounts_csv(accounts)
          save_transaction_history_csv(account)
        else:
          print("Account not found!")
      except ValueError:
        print("Invalid amount. Please enter a valid number.")

    elif choice == "3":
      acc_num = input("Enter account number: ")
      password = getpass.getpass("Enter account password: ")
      amount = input("Enter withdrawal amount: ")
      try:
        amount = float(amount)
        account = BankAccount.find_account(accounts, acc_num)
        if account and account.verify_password(password):
          result = account.withdraw(amount, password)
          print(result)
          if "Invalid" not in result:
            save_accounts_csv(accounts)
            save_transaction_history_csv(account)
        elif account:
          print("Incorrect password. Withdrawal denied.")
        else:
          print("Account not found!")
      except ValueError:
        print("Invalid amount. Please enter a valid number.")

    elif choice == "4":
      acc_num = input("Enter account number: ")
      password = getpass.getpass("Enter account password: ")
      account = BankAccount.find_account(accounts, acc_num)
      if account and account.verify_password(password):
        print(account.get_balance())
      elif account:
        print("Incorrect password. Access denied.")
      else:
        print("Account not found!")

    elif choice == "5":
      acc_num = input("Enter account number: ")
      password = getpass.getpass("Enter account password: ")
      account = BankAccount.find_account(accounts, acc_num)
      if account and account.verify_password(password):
        transaction_history = account.get_transaction_history()
        if transaction_history:
          print(f"\nTransaction History for Account {acc_num}:")
          for date, description in transaction_history:
            print(f"{date.strftime('%Y-%m-%d %H:%M:%S')}: {description}")
        else:
          print("No transactions recorded for this account.")
      elif account:
        print("Incorrect password. Access denied.")
      else:
        print("Account not found!")

    elif choice == "6":
      print("Exiting program. Thank you!")
      break

    else:
      print("Invalid choice. Please enter a number between 1 and 6.")
