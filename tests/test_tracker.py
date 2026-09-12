import os
from pathlib import Path

from expense_tracker import data


def test_budget_and_summary(tmp_path, monkeypatch):
    db_path = tmp_path / "expense_tracker.db"
    monkeypatch.setattr(data, "DB_FILE", db_path)
    data.init_db()

    data.add_transaction("Expense", "Food", 250.0, "Lunch", "2026-09-12")
    data.add_transaction("Income", "Salary", 1200.0, "Monthly pay", "2026-09-12")
    data.set_budget(900.0)

    transactions = data.list_transactions()
    summary = data.get_summary()

    assert len(transactions) == 2
    assert summary["income"] == 1200.0
    assert summary["expense"] == 250.0
    assert summary["balance"] == 950.0
    assert data.get_budget() == 900.0
