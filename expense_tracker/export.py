from data import load_data

def export_to_csv():
    transactions = load_data()

    if not transactions:
        print("\nNo data to export.")
        return

    with open("expenses_export.csv", "w") as file:
        file.write("Date,Type,Category,Amount,Note\n")
        for t in transactions:
            file.write(f"{t['date']},{t['type']},{t['category']},{t['amount']},{t['note']}\n")

    print("\n✅ Data exported successfully to 'expenses_export.csv'")