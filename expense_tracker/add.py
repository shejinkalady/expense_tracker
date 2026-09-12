from datetime import datetime
from data import load_data, save_data
from budget import check_budget

def add_transaction():
    transactions = load_data()

    print("\n" + "="*40)
    print("       ADD TRANSACTION")
    print("="*40)

    t_type = input("Type (Income/Expense): ").capitalize()
    while t_type not in ["Income", "Expense"]:
        print("Please enter only Income or Expense!")
        t_type = input("Type (Income/Expense): ").capitalize()

    category = input("Category: ").title()
    amount = float(input("Amount: ₹"))
    note = input("Note (optional): ")
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    transaction = {
        "date": date,
        "type": t_type,
        "category": category,
        "amount": amount,
        "note": note
    }

    transactions.append(transaction)
    save_data(transactions)
    print("\n✅ Transaction added successfully!")

    if t_type == "Expense":
        check_budget()