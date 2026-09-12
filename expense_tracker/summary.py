from data import load_data, load_budget

def show_summary():
    transactions = load_data()
    budget_data = load_budget()
    monthly_budget = budget_data.get("monthly_budget", 0)

    income = 0
    expense = 0
    category_totals = {}

    for t in transactions:
        if t['type'] == "Income":
            income += t['amount']
        else:
            expense += t['amount']

        category_totals[t['category']] = category_totals.get(t['category'], 0) + t['amount']

    balance = income - expense

    print("\n" + "="*45)
    print(" FINANCIAL SUMMARY")
    print("="*45)
    print(f"Total Income     : ₹{income}")
    print(f"Total Expense    : ₹{expense}")
    print(f"Balance          : ₹{balance}")

    if monthly_budget > 0:
        print("-"*45)
        print(f"Monthly Budget   : ₹{monthly_budget}")
        remaining = monthly_budget - expense
        if remaining >= 0:
            print(f"Remaining Budget : ₹{remaining}")
        else:
            print(f"⚠️  Overspent     : ₹{abs(remaining)}")

    print("="*45)

    print("\nCategory-wise Summary:")
    print("-"*35)
    for cat, total in category_totals.items():
        print(f"{cat:<22} : ₹{total}")