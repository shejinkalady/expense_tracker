from data import load_data

def view_transactions():
    transactions = load_data()

    print("\n" + "="*70)
    print("ALL TRANSACTIONS")
    print("="*70)

    if not transactions:
        print("No transactions found.")
        return

    print(f"{'No.':<5}{'Date':<18}{'Type':<10}{'Category':<15}{'Amount':<12}Note")
    print("-"*70)

    for i, t in enumerate(transactions, 1):
        print(f"{i:<5}{t['date']:<18}{t['type']:<10}{t['category']:<15}₹{t['amount']:<11}{t['note']}")