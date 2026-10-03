import json
from pathlib import Path

DATA_FILE = Path("expenses.json")


def load_expenses():
    """Load expenses from the JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read expense data. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def get_amount():
    """Get a valid positive expense amount."""
    while True:
        try:
            amount = float(input("Enter amount (Rs.): "))
            if amount > 0:
                return amount
            print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def add_expense(expenses):
    """Add a new expense."""
    name = input("Enter expense name: ").strip()
    category = input("Enter category: ").strip()

    if not name or not category:
        print("Name and category cannot be empty.")
        return

    amount = get_amount()

    expense = {
        "name": name,
        "amount": amount,
        "category": category
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully.")


def view_expenses(expenses):
    """Display all expenses."""
    if not expenses:
        print("No expenses found.")
        return

    print("\n" + "=" * 55)
    print(f"{'No.':<5}{'Name':<20}{'Amount':<15}{'Category':<15}")
    print("=" * 55)

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index:<5}"
            f"{expense['name'][:19]:<20}"
            f"Rs.{expense['amount']:<12.2f}"
            f"{expense['category'][:14]:<15}"
        )

    print("=" * 55)


def total_expense(expenses):
    """Display total spending."""
    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal Expense: Rs.{total:.2f}")


def category_expense(expenses):
    """Display spending for a selected category."""
    if not expenses:
        print("No expenses found.")
        return

    category = input("Enter category: ").strip().lower()

    total = sum(
        expense["amount"]
        for expense in expenses
        if expense["category"].lower() == category
    )

    print(f"Total {category.title()} Expense: Rs.{total:.2f}")


def delete_expense(expenses):
    """Delete an expense by its number."""
    if not expenses:
        print("No expenses found.")
        return

    view_expenses(expenses)

    try:
        number = int(input("Enter expense number to delete: "))
        if 1 <= number <= len(expenses):
            deleted = expenses.pop(number - 1)
            save_expenses(expenses)
            print(f"Deleted: {deleted['name']}")
        else:
            print("Invalid expense number.")
    except ValueError:
        print("Please enter a valid number.")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 40)
    print("        EXPENSE MANAGER")
    print("=" * 40)
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Category Expense")
    print("5. Delete Expense")
    print("6. Exit")
    print("=" * 40)


def main():
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            total_expense(expenses)
        elif choice == "4":
            category_expense(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            print("Thanks for using Expense Manager!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
