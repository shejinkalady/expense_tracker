from data import load_budget, save_budget, load_data

def set_budget():
    print("\n" + "="*40)
    print("SET MONTHLY BUDGET")
    print("="*40)

    try:
        amount = float(input("Enter Monthly Budget (₹): "))
        save_budget({"monthly_budget": amount})
        print(f"\n✅ Monthly Budget set to ₹{amount}")
    except:
        print("Invalid amount!")

def view_budget():
    budget = load_budget()
    amount = budget.get("monthly_budget", 0)
    print("\n" + "="*40)
    print(f"Current Monthly Budget: ₹{amount}")
    print("="*40)

def check_budget():
    transactions = load_data()
    budget_data = load_budget()
    monthly_budget = budget_data.get("monthly_budget", 0)

    if monthly_budget == 0:
        return

    total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")

    if total_expense > monthly_budget:
        print("\n⚠️  WARNING: You have exceeded your monthly budget!")
        print(f"Budget    : ₹{monthly_budget}")
        print(f"Spent     : ₹{total_expense}")
        print(f"Overspent : ₹{total_expense - monthly_budget}")
    else:
        remaining = monthly_budget - total_expense
        print(f"\n💰 Remaining Budget: ₹{remaining}")