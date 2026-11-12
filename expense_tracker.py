
import csv
import os
from datetime import date

FILE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "expenses.csv"
)

HEADERS = ["Date", "Category", "Amount", "Description"]


def create_file():
    if not os.path.exists(FILE_NAME) or os.path.getsize(FILE_NAME) == 0:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(HEADERS)


def read_expenses():
    expenses = []

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("CSV file is empty or has no header.")
                return expenses

            # Normalize column names
            reader.fieldnames = [
                name.strip().lstrip("\ufeff") if name else ""
                for name in reader.fieldnames
            ]

            if reader.fieldnames != HEADERS:
                print("CSV header is incorrect.")
                print("Expected:", ",".join(HEADERS))
                print("Found:", ",".join(reader.fieldnames))
                return expenses

            for row in reader:
                try:
                    expenses.append({
                        "Date": (row.get("Date") or "").strip(),
                        "Category": (row.get("Category") or "").strip(),
                        "Amount": float(row.get("Amount") or 0),
                        "Description": (row.get("Description") or "").strip()
                    })
                except (ValueError, AttributeError):
                    print("Skipping an invalid expense row.")

    except FileNotFoundError:
        create_file()

    return expenses


def add_expense():
    print("\n===== ADD EXPENSE =====")

    category = input("Enter category (Food/Travel/Shopping): ").strip().title()
    if not category:
        print("Category cannot be empty!")
        return

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero!")
            return
    except ValueError:
        print("Please enter a valid number!")
        return

    description = input("Enter description: ").strip()
    expense_date = date.today().isoformat()

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([expense_date, category, amount, description])

    print("Expense added successfully!")


def view_expenses():
    print("\n===== ALL EXPENSES =====")
    expenses = read_expenses()

    if not expenses:
        print("No expenses found.")
        return

    for expense in expenses:
        print(
            f"Date: {expense['Date']} | "
            f"Category: {expense['Category']} | "
            f"Amount: Rs. {expense['Amount']:.2f} | "
            f"Description: {expense['Description']}"
        )


def filter_expenses():
    category = input("Enter category to filter: ").strip().lower()
    expenses = read_expenses()
    found = False

    print(f"\n===== {category.upper()} EXPENSES =====")

    for expense in expenses:
        if expense["Category"].lower() == category:
            print(
                f"Date: {expense['Date']} | "
                f"Category: {expense['Category']} | "
                f"Amount: Rs. {expense['Amount']:.2f} | "
                f"Description: {expense['Description']}"
            )
            found = True

    if not found:
        print("No expenses found in this category.")


def category_summary():
    expenses = read_expenses()
    totals = {}

    for expense in expenses:
        category = expense["Category"]
        totals[category] = totals.get(category, 0) + expense["Amount"]

    print("\n===== CATEGORY SUMMARY =====")

    if not totals:
        print("No expenses available.")
        return

    for category, total in totals.items():
        print(f"{category}: Rs. {total:.2f}")

    print(f"Total expenses: Rs. {sum(totals.values()):.2f}")


def main():
    create_file()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses by Category")
        print("4. Category Summary")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice! Please enter 1-5.")


if __name__ == "__main__":
    main()
