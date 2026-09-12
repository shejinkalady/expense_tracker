import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "expense_tracker.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT DEFAULT ''
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            monthly_budget REAL DEFAULT 0
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target REAL NOT NULL,
            current REAL DEFAULT 0,
            color TEXT DEFAULT '#1d4ed8'
        )
        """
    )
    conn.execute(
        "INSERT OR IGNORE INTO budget (id, monthly_budget) VALUES (1, 0)"
    )
    conn.commit()
    conn.close()


init_db()


def list_transactions():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, date, type, category, amount, note FROM transactions ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_transaction(transaction_type, category, amount, note="", date=None):
    transaction_type = str(transaction_type).strip()
    category = str(category).strip() or "General"
    amount = float(amount)
    note = str(note or "").strip()
    date_value = date or datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO transactions (date, type, category, amount, note) VALUES (?, ?, ?, ?, ?)",
        (date_value, transaction_type, category, amount, note),
    )
    conn.commit()
    item = dict(
        id=cursor.lastrowid,
        date=date_value,
        type=transaction_type,
        category=category,
        amount=amount,
        note=note,
    )
    conn.close()
    return item


def delete_transaction(index):
    rows = list_transactions()
    if 0 <= index < len(rows):
        transaction_id = rows[index]["id"]
        conn = get_connection()
        conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()
        return rows[index]
    return None


def edit_transaction(index, transaction_type=None, category=None, amount=None, note=None, date=None):
    rows = list_transactions()
    if 0 <= index < len(rows):
        row = rows[index]
        updated = {
            "type": transaction_type if transaction_type is not None else row["type"],
            "category": category if category is not None else row["category"],
            "amount": float(amount) if amount is not None else float(row["amount"]),
            "note": note if note is not None else row["note"],
            "date": date if date is not None else row["date"],
        }
        conn = get_connection()
        conn.execute(
            "UPDATE transactions SET type = ?, category = ?, amount = ?, note = ?, date = ? WHERE id = ?",
            (updated["type"], updated["category"], updated["amount"], updated["note"], updated["date"], row["id"]),
        )
        conn.commit()
        conn.close()
        return updated
    return None


def load_budget():
    conn = get_connection()
    row = conn.execute("SELECT monthly_budget FROM budget WHERE id = 1").fetchone()
    conn.close()
    return {"monthly_budget": float(row[0]) if row else 0}


def save_budget(budget):
    conn = get_connection()
    conn.execute("UPDATE budget SET monthly_budget = ? WHERE id = 1", (float(budget.get("monthly_budget", 0) or 0),))
    conn.commit()
    conn.close()


def get_budget():
    return float(load_budget().get("monthly_budget", 0) or 0)


def set_budget(amount):
    save_budget({"monthly_budget": float(amount)})
    return float(amount)


def get_summary():
    transactions = list_transactions()
    income = 0.0
    expense = 0.0
    category_totals = {}
    for item in transactions:
        amount = float(item.get("amount", 0) or 0)
        category = item.get("category", "General")
        if item.get("type") == "Income":
            income += amount
        elif item.get("type") == "Expense":
            expense += amount
        category_totals[category] = category_totals.get(category, 0.0) + amount

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense,
        "category_totals": category_totals,
        "transactions_count": len(transactions),
    }


def search_transactions(keyword="", transaction_type="All"):
    keyword = str(keyword or "").strip().lower()
    conn = get_connection()
    if keyword and transaction_type != "All":
        rows = conn.execute(
            "SELECT id, date, type, category, amount, note FROM transactions WHERE (LOWER(category) LIKE ? OR LOWER(note) LIKE ? OR LOWER(date) LIKE ?) AND type = ? ORDER BY id DESC",
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", transaction_type),
        ).fetchall()
    elif keyword:
        rows = conn.execute(
            "SELECT id, date, type, category, amount, note FROM transactions WHERE LOWER(category) LIKE ? OR LOWER(note) LIKE ? OR LOWER(date) LIKE ? ORDER BY id DESC",
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        ).fetchall()
    elif transaction_type != "All":
        rows = conn.execute(
            "SELECT id, date, type, category, amount, note FROM transactions WHERE type = ? ORDER BY id DESC",
            (transaction_type,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT id, date, type, category, amount, note FROM transactions ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_goal(name, target, current=0, color="#1d4ed8"):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO goals (name, target, current, color) VALUES (?, ?, ?, ?)",
        (str(name).strip(), float(target), float(current), str(color)),
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid


def list_goals():
    conn = get_connection()
    rows = conn.execute("SELECT id, name, target, current, color FROM goals ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_goal(goal_id, name=None, target=None, current=None, color=None):
    goals = list_goals()
    for goal in goals:
        if goal["id"] == goal_id:
            conn = get_connection()
            conn.execute(
                "UPDATE goals SET name = ?, target = ?, current = ?, color = ? WHERE id = ?",
                (
                    str(name or goal["name"]).strip(),
                    float(target if target is not None else goal["target"]),
                    float(current if current is not None else goal["current"]),
                    str(color or goal["color"]),
                    goal_id,
                ),
            )
            conn.commit()
            conn.close()
            return True
    return False


def delete_goal(goal_id):
    conn = get_connection()
    conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()


def add_goal_from_transaction(category, amount):
    match = str(category).strip()
    if not match:
        return
    goals = list_goals()
    for goal in goals:
        if goal["name"].lower() == match.lower():
            update_goal(goal["id"], current=float(goal["current"]) + float(amount))
            return
    add_goal(match, target=max(float(amount), 100.0), current=float(amount), color="#10b981")


if __name__ == "__main__":
    init_db()