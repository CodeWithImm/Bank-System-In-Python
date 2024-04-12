import sys
from time import gmtime, strftime

class Bank:
    def __init__(self):
        # Load account record
        try:
            with open("Accnt_Record.txt", 'r') as f:
                self.next_account_number = int(f.readline()) + 1
        except FileNotFoundError:
            self.next_account_number = 1

    def bank_system(self):
        while True:
            print("\nLets Try My Feature")
            print("Whatcha wanna do today?")
            print("1) Create a brand new account")
            print("2) Deposit some cash into your account")
            print("3) Withdraw some cash from your account")
            print("4) Check your account balance")
            print("5) See your transaction history")
            choice = int(input("Pick an option: "))

            if choice == 1:
                name = input("What's your name? ")
                opening_balance = float(input("\nAlright, how much do you wanna start with? "))
                self.create_account(name, opening_balance)
            elif choice in [2, 3, 4, 5]:
                name = input("What's your name again? ")
                acc_no = input("\nAnd your account number? ")

                # Verifikasi PIN dengan pesan yang lebih kasual
                if not self.verify_pin(acc_no):
                    print("Whoops! The PIN is wrong. You have more tries left.")
                    continue

                if choice == 2:
                    amount = float(input("\nHow much moolah do you wanna deposit? "))
                    self.credit(acc_no, name, amount)
                elif choice == 3:
                    amount = float(input("\nHow much cash do you wanna take out? "))
                    self.debit(acc_no, name, amount)
                elif choice == 4:
                    self.check_balance(acc_no)
                elif choice == 5:
                    self.transaction_history(acc_no)
                
            print("\nThanks for banking with us!")
            continue_program = input("Wanna do something else? (y/n): ")
            if continue_program.lower() == 'n':
                break

    def verify_pin(self, acc_no):
        try:
            with open(f"{acc_no}-pin.txt", 'r') as f:
                stored_pin = f.readline().strip()
            pin_attempts = 3
            while pin_attempts > 0:
                pin = input("Enter your PIN (4 digits): ")
                if pin == stored_pin:
                    return True
                pin_attempts -= 1
                print(f"Uh oh! The PIN is wrong. Don't sweat it, you have {pin_attempts} more tries.")
            return False
        except FileNotFoundError:
            print(f"Account number {acc_no} not found.")
            return False

    def create_account(self, name, opening_balance):
        acc_no = self.next_account_number
        pin = input("Set your 4-digit ATM PIN: ")
        if len(pin) != 4 or not pin.isdigit():
            print("PIN must be 4 digits.")
            return

        with open(f"{acc_no}-pin.txt", 'w') as f:
            f.write(pin)

        with open(f"{acc_no}.txt", 'w') as f:
            f.write(f"{opening_balance}\n{name}\n{acc_no}\n")

        with open(f"{acc_no}-rec.txt", 'w') as f:
            f.write("Date\t\t\t\tCredit\tDebit\tBalance\n")
            f.write(f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())}\t{opening_balance}\t0\t{opening_balance}\n")

        print(f"\nSweet! Your account is all set. Your account number is {acc_no}.")

        with open("Accnt_Record.txt", 'w') as f:
            f.write(str(self.next_account_number))
        
        self.next_account_number += 1

    def credit(self, acc_no, name, amount):
        balance = self.update_balance(acc_no, name, amount)
        if balance is not None:
            print(f"\nNice! You just deposited {amount}. Your current balance is {balance}.")

    def debit(self, acc_no, name, amount):
        balance = self.update_balance(acc_no, name, -amount)
        if balance is not none:
            print(f"\nYou've just withdrawn {amount}. Your current balance is {balance}.")

    def check_balance(self, acc_no):
        try:
            with open(f"{acc_no}.txt", 'r') as f:
                balance = float(f.readline().strip())
            print(f"\nYour current balance is: {balance}")
        except FileNotFoundError:
            print(f"Uh oh! Account number {acc_no} doesn't exist.")

    def transaction_history(self, acc_no):
        try:
            with open(f"{acc_no}-rec.txt", 'r') as f:
                print("\nHere's your transaction history:")
                for line in f:
                    print(line.strip())
        except FileNotFoundError:
            print(f"Account number {acc_no} not found.")

    def update_balance(self, acc_no, name, amount):
        try:
            with open(f"{acc_no}.txt", 'r+') as f:
                current_balance = float(f.readline().strip())
                if amount < 0 and current_balance + amount < 0:
                    print("Oops! Insufficient balance for this transaction.")
                    return None
                
                new_balance = current_balance + amount
                f.seek(0)
                f.write(f"{new_balance}\n{name}\n{acc_no}\n")
                f.truncate()
                
            with open(f"{acc_no}-rec.txt", 'a') as f:
                f.write(f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())}\t{amount if amount >= 0 else '0'}\t{abs(amount) if amount < 0 else '0'}\t{new_balance}\n")
            
            return new_balance
        except FileNotFoundError:
            print(f"Account number {acc_no} not found.")
            return None

if __name__ == '__main__':
    print("Yo! Welcome to Jonathan Bank!")
    bank = Bank()
    bank.bank_system()
