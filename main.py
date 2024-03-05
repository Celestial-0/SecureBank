import csv
import getpass
from Account import BankAccount, save_accounts_csv, save_transaction_history_csv, load_accounts_csv

def main():
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

if __name__ == "__main__":
  main()
