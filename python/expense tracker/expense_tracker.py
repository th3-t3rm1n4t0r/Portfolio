import csv, os
from datetime import date
from tabulate import tabulate
from babel.numbers import get_currency_symbol
import matplotlib.pyplot as plt
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import time
console = Console()

EXPENSE_FILE = "expenses.csv"
INCOME_FILE = "income.csv"
LOG_FILE = "logs.csv"
CONFIG_FILE = "config.txt"

def main():
    splash_title = Text("Welcome to Expense Tracker!", style = "bold cyan", justify = "center")
    splash_body = Align.center(
        """[bold white]
        Track your income and expenses with ease!
        Developed in Python by Abhishek Karmakar
        [/bold white]""", vertical = "middle")
    console.print(Panel(splash_body, title = splash_title, border_style = "cyan", expand = "False"))
    time.sleep(1.5)

    initialize_files()
    currency = get_currency()

    while True:
        title = Text("EXPENSE TRACKER - MAIN MENU", style = "bold cyan", justify = "center")
        body = """[bold white]
[1] Add Income
[2] Add Expense
[3] View Summary
[4] View Graph
[5] Help
[6] Reset Data
[0] Exit
[/bold white]"""
        wrapped_body = Align.center(body, vertical = "middle")
        console.print(Panel(wrapped_body, title = title, border_style = "cyan", expand = False))

        try:
            choice = int(input("Enter your choice: "))
            if choice == 0:
                raise EOFError
            elif choice == 1:
                add_income(currency)
                print()
                continue
            elif choice == 2:
                add_expense(currency)
                print()
                continue
            elif choice == 3:
                show_summary(currency)

                print("\nPress Enter to exit", end = "")
                e = input()
                if e == "":
                    continue
            elif choice == 4:
                view_graph(None)

                print("\nPress Enter to exit", end = "")
                e = input()
                if e == "":
                    continue
            elif choice == 5:
                show_help()

                print("\nPress Enter to exit", end = "")
                e = input()
                if e == "":
                    continue
            elif choice == 6:
                console.print("[bold red]All files will be deleted and you'll have to start afresh.[/bold red]")
                con = input("Type 'RESET' to confirm: ").strip()
                if con == "RESET":
                    files_to_remove = [EXPENSE_FILE, INCOME_FILE, LOG_FILE, CONFIG_FILE]
                    for file in files_to_remove:
                        os.remove(file)
                        console.print(f"[green]Removed {file}[/green]")
                    console.print("[green]All data was removed successfully.[/green]")
                    initialize_files()
                    get_currency()
                    continue
                else:
                    continue
            else:
                console.print("[bold yellow]Invalid choice. Try again.[/bold yellow]")
        except EOFError:
            console.print("[bold cyan]\nExiting program...[/bold cyan]")
            break
        except ValueError:
            console.print("[bold yellow]Please enter a number...[/bold yellow]")

def initialize_files():
    try:
        open(INCOME_FILE, "x").write("Month,Date,Income\n")
        open(EXPENSE_FILE, "x").write("Month,Date,Amount,Category\n")
        open(LOG_FILE, "x").write("Date,Message\n")
        print("✅ Created 'income.csv', 'expense.csv' and 'logs.csv' successfully.")
    except FileExistsError:
        print("✅ 'income.csv', 'expense.csv' and 'logs.csv' already exist.")

def get_currency():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as file:
            currency = file.read().strip()
            if currency:
                symbol = get_currency_symbol(currency)
                print("✅ 'config.txt' exists.")
                print(f"Using saved Currency: {symbol}")
                return symbol
    else:
        while True:
            currency = input("Enter your preferred currency: ")
            try:
                symbol = get_currency_symbol(currency)
                if symbol == currency:
                    raise ValueError
            except ValueError:
                print("Invalid currency. Try again.")
            else:
                with open(CONFIG_FILE, "w") as file:
                    file.write(currency)
                print(f"Currency set to {currency} ({symbol})")
                return symbol

def add_income(curr):
    income = int(input("Enter current month's Income: "))
    dat = date.today()
    mon = dat.strftime("%B %Y")

    with open(INCOME_FILE, "a") as file0:
        writer = csv.DictWriter(file0, fieldnames = ["Month", "Date", "Income"])
        writer.writerow({"Month" : mon, "Date" : dat, "Income" : income})
    
    with open(LOG_FILE, "a") as file1:
        writer = csv.DictWriter(file1, fieldnames = ["Date", "Message"])
        writer.writerow({"Date" : dat, "Message" : f"Income of {curr}{income} was added successfully on {dat}."})
    print(f"Income of {curr}{income} was added successfully on {dat}.")
    return

def add_expense(curr):
    dat = date.today()
    mon = dat.strftime("%B %Y")
    amount = int(input("Enter the amount you spent: "))
    cat = input("What did you spend on?: ")

    with open(EXPENSE_FILE, "a") as file0:
        writer = csv.DictWriter(file0, fieldnames = ["Month", "Date", "Amount", "Category"])
        writer.writerow({"Month" : mon, "Date" : dat, "Amount" : amount, "Category" : cat})
    
    with open(LOG_FILE, "a") as file1:
        writer = csv.DictWriter(file1, fieldnames = ["Date", "Message"])
        writer.writerow({"Date" : dat, "Message" : f"Expense of {curr}{amount} on {cat} was added successfully on {dat}."})
    print(f"Expense of {curr}{amount} on {cat} was added successfully on {dat}.")
    return

def show_summary(curr):
    months = set()
    with open(EXPENSE_FILE) as file0:
        reader = csv.DictReader(file0)
        for row in reader:
            months.add(row["Month"])

    print("\n=======Available Months=======")
    for m in sorted(months):
        print("-", m)
    mon = input("Enter month and year to view summary: ")
    if mon in months:
        inc = []
        exp = []
        GREEN = "\033[92m"
        RED = "\033[91m"
        RESET = "\033[0m"
        with open(INCOME_FILE) as file0:
            reader = csv.DictReader(file0)
            for row in reader:
                if row["Month"] == mon:
                    inc.append([row["Date"], float(row["Income"])])
        header = ["Date", f"Income in {curr}"]
        print(f"\n=======Income for {mon}=======")
        print(tabulate(inc, headers = header, tablefmt = "fancy_grid"))
        
        with open(EXPENSE_FILE) as file1:
            reader = csv.DictReader(file1)
            for row in reader:
                if row["Month"] == mon:
                    exp.append([row["Date"], float(row["Amount"]), row["Category"]])
        header = ["Date", f"Amount in {curr}", "Category"]
        print(f"\n=======Expenses for {mon}=======")
        print(tabulate(exp, headers = header, tablefmt = "fancy_grid"))

        total_inc = sum(float(s[1]) for s in inc)
        total_exp = sum(float(r[1]) for r in exp)
        print(f"Total Expense in {mon}: {total_exp}")
        saved = total_inc - total_exp

        if saved >= 0:
            print(f"Savings in {mon}: {GREEN}{curr}{saved:.2f}{RESET}")
        else:
            print(f"Overspending in {mon}: {RED}{curr}{abs(saved):.2f}{RESET}")
    else:
        print(f"No expenses found for {mon}")

def view_graph(expense):
    print("Not added yet, try another feature")

def show_help():
    title = Text("EXPENSE TRACKER - HELP MENU", style = "bold cyan", justify = "center")
    body = """[bold white]
    Welcome to your Expense Tracker!
    You can use this app to track how your money is credited or debited. You can also see a summary and a graph showing your expenditure.
    This app was developed after I managed to spend 500 before the month was even over. I hope this can help you develop a healthy relationship with money just like I did.
    Now, let's look at the menu.
          
    [bold green] MENU OPTIONS: [/bold green]
    1. Add Income - Here you add how much was credited to your account.
    2. Add Expense - Here you add how much was debitted from your account.
    3. View Summary - Here, you get a summary of the credit and debit and also how much you saved and how much was spent.
    4. View Graph - Here, a graph is plotted showing how much was saved each month.
    5. Help - Here, you'll get this exact menu.
    6. Reset Data - Removes all files and starts afresh.
    0. Exit - And here, you exit the app. Note that pressing Ctrl-D gives similar results.
    [italic]Tip:[/italic] Press ENTER when prompted to return to the main menu.
    And that's about it!
    [bold green]Save smart and spend wiser💸💸[/bold green]
    [/bold white]"""
    
    wrapped_body = Align.center(body, vertical = "middle")
    console.print(Panel(wrapped_body, title = title, expand = False, border_style = "cyan"))

if __name__ == "__main__":
    main()