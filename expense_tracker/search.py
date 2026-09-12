from data import load_data

def search_transactions():
    transactions = load_data()

    print("\n" + "="*40)
    print("SEARCH / FILTER")
    print("="*40)
    print("1. Search by Category")
    print("2. Search by Date")
    print("3. Monthly Filter")
    print("4. Back")

    choice = input("Enter choice: ")

    if choice == "1":
        cat = input("Enter Category: ").title()
        found = [t for t in transactions if t['category'] == cat]
    elif choice == "2":
        date = input("Enter Date (DD-MM-YYYY): ")
        found = [t for t in transactions if t['date'].startswith(date)]
    elif choice == "3":
        month = input("Enter Month (MM-YYYY): ")
        found = [t for t in transactions if month in t['date']]
    else:
        return

    print("\n" + "="*70)
    if not found:
        print("No transactions found.")
        return

    print(f"{'Date':<18}{'Type':<10}{'Category':<15}{'Amount':<12}Note")
    print("-"*70)
    for t in found:
        print(f"{t['date']:<18}{t['type']:<10}{t['category']:<15}₹{t['amount']:<11}{t['note']}")