from data import load_data, save_data
from view import view_transactions

def edit_transaction():
    transactions = load_data()
    view_transactions()

    if not transactions:
        return

    try:
        num = int(input("\nEnter transaction number to edit: "))
        if 1 <= num <= len(transactions):
            t = transactions[num - 1]

            print("\nLeave blank if you don't want to change.")
            new_type = input(f"Type ({t['type']}): ").capitalize() or t['type']
            new_category = input(f"Category ({t['category']}): ").title() or t['category']
            new_amount = input(f"Amount (₹{t['amount']}): ")
            new_note = input(f"Note ({t['note']}): ") or t['note']

            t['type'] = new_type if new_type in ["Income", "Expense"] else t['type']
            t['category'] = new_category
            t['amount'] = float(new_amount) if new_amount else t['amount']
            t['note'] = new_note

            save_data(transactions)
            print("\n✅ Transaction updated successfully!")
        else:
            print("Invalid number!")
    except:
        print("Something went wrong!")