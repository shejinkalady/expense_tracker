from data import load_data, save_data
from view import view_transactions

def delete_transaction():
    transactions = load_data()
    view_transactions()

    if not transactions:
        return

    try:
        num = int(input("\nEnter transaction number to delete: "))
        if 1 <= num <= len(transactions):
            removed = transactions.pop(num - 1)
            save_data(transactions)
            print(f"\n✅ Deleted: {removed['type']} - ₹{removed['amount']}")
        else:
            print("Invalid number!")
    except:
        print("Please enter a valid number!")