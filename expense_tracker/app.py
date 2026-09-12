import csv
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from expense_tracker.data import (
    add_goal,
    add_transaction,
    delete_goal,
    delete_transaction,
    edit_transaction,
    get_budget,
    get_summary,
    list_goals,
    list_transactions,
    search_transactions,
    set_budget,
    update_goal,
)


class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.geometry("540x270+420+180")
        self.configure(bg="#120f1d")

        gradient = tk.Canvas(self, width=540, height=270, bg="#120f1d", highlightthickness=0)
        gradient.pack(fill="both", expand=True)
        gradient.create_rectangle(0, 0, 540, 270, fill="#120f1d", outline="")
        gradient.create_oval(170, 30, 370, 230, fill="#c8a96b", outline="")
        gradient.create_oval(205, 60, 335, 190, fill="#0e1728", outline="")
        gradient.create_text(270, 123, text="N", fill="#f7e7b5", font=("Segoe UI", 46, "bold"))
        gradient.create_text(270, 210, text="NOVA LUXE BUDGET", fill="#f8ecd0", font=("Segoe UI", 20, "bold"))
        self.after(1800, self.destroy)


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nova Luxe Budget")
        self.geometry("1320x780")
        self.minsize(1160, 700)
        self.configure(bg="#f5f5f7")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f5f5f7")
        self.style.configure("TLabel", background="#f5f5f7", foreground="#1d1d1f", font=("SF Pro Display", 10))
        self.style.configure("TEntry", fieldbackground="#ffffff", foreground="#1d1d1f", insertcolor="#1d1d1f")
        self.style.configure("TCombobox", fieldbackground="#ffffff", foreground="#1d1d1f")
        self.style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="#1d1d1f", rowheight=30)
        self.style.configure("Treeview.Heading", background="#f0f0f2", foreground="#1d1d1f", font=("SF Pro Display", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#dfeaff")], foreground=[("selected", "#111111")])

        self.splash = SplashScreen(self)
        self.splash.wait_visibility()

        self.bg_canvas = tk.Canvas(self, width=100, height=100, highlightthickness=0, bg="#f5f5f7")
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.orbs = [
            {"x": 200, "y": 180, "r": 180, "dx": 0.6, "dy": 0.4, "color": "#dfeaff"},
            {"x": 980, "y": 260, "r": 220, "dx": -0.7, "dy": 0.5, "color": "#e3d8ff"},
            {"x": 710, "y": 620, "r": 260, "dx": 0.8, "dy": -0.6, "color": "#d7f5ea"},
            {"x": 240, "y": 540, "r": 150, "dx": -0.5, "dy": -0.4, "color": "#fff2d4"},
        ]
        self.after(40, self.animate_background)

        self.main_container = tk.Frame(self, bg="#f5f5f7", padx=20, pady=18, bd=0)
        self.main_container.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        self.sidebar = tk.Frame(self.main_container, bg="#ffffff", padx=18, pady=20, bd=0)
        self.sidebar.pack(side="left", fill="y")

        tk.Label(self.sidebar, text="NOVA", bg="#ffffff", fg="#1d1d1f", font=("SF Pro Display", 28, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Label(self.sidebar, text="LUXE BUDGET", bg="#ffffff", fg="#6e6e73", font=("SF Pro Display", 11, "bold")).pack(anchor="w", pady=(0, 28))

        for label, cmd in [
            ("Overview", lambda: self.show_tab("overview")),
            ("Transactions", lambda: self.show_tab("transactions")),
            ("Goals", lambda: self.show_tab("goals")),
        ]:
            btn = tk.Button(
                self.sidebar,
                text=label,
                command=cmd,
                bg="#f2f2f4",
                fg="#1d1d1f",
                activebackground="#dfeaff",
                activeforeground="#111111",
                relief="flat",
                bd=0,
                padx=14,
                pady=12,
                width=18,
                font=("SF Pro Display", 11, "bold"),
            )
            btn.pack(fill="x", pady=8)

        self.content = tk.Frame(self.main_container, bg="#f5f5f7")
        self.content.pack(side="left", fill="both", expand=True)

        self.tabs = {}
        self._build_overview_tab()
        self._build_transactions_tab()
        self._build_goals_tab()
        self.show_tab("overview")
        self.refresh_all()

    def animate_background(self):
        w = self.winfo_width()
        h = self.winfo_height()
        self.bg_canvas.delete("all")
        self.bg_canvas.create_rectangle(0, 0, w, h, fill="#090b12", outline="")

        for orb in self.orbs:
            orb["x"] += orb["dx"]
            orb["y"] += orb["dy"]
            if orb["x"] < -orb["r"] or orb["x"] > w + orb["r"]:
                orb["dx"] *= -1
            if orb["y"] < -orb["r"] or orb["y"] > h + orb["r"]:
                orb["dy"] *= -1
            self.bg_canvas.create_oval(
                orb["x"] - orb["r"], orb["y"] - orb["r"], orb["x"] + orb["r"], orb["y"] + orb["r"],
                fill=orb["color"], outline="", stipple="gray25"
            )
            self.bg_canvas.create_oval(
                orb["x"] - orb["r"] * 0.55, orb["y"] - orb["r"] * 0.55,
                orb["x"] + orb["r"] * 0.55, orb["y"] + orb["r"] * 0.55,
                fill="#f7e7b5", outline="", stipple="gray12"
            )
        self.after(30, self.animate_background)

    def show_tab(self, name):
        for frame in self.tabs.values():
            frame.pack_forget()
        if name in self.tabs:
            self.tabs[name].pack(fill="both", expand=True)

    def _build_overview_tab(self):
        frame = tk.Frame(self.content, bg="#f5f5f7")
        self.tabs["overview"] = frame

        tk.Label(frame, text="Financial Overview", bg="#f5f5f7", fg="#1d1d1f", font=("SF Pro Display", 24, "bold")).pack(anchor="w", padx=18, pady=(18, 12))

        cards = tk.Frame(frame, bg="#f5f5f7")
        cards.pack(fill="x", padx=18)

        self.overview_cards = {}
        for label, key in [("Income", "income"), ("Expense", "expense"), ("Balance", "balance"), ("Budget", "budget")]:
            card = tk.Frame(cards, bg="#ffffff", padx=18, pady=18)
            card.pack(side="left", fill="y", expand=True, padx=(0, 12))
            tk.Label(card, text=label, bg="#ffffff", fg="#6e6e73", font=("SF Pro Display", 10, "bold")).pack(anchor="w")
            value = tk.StringVar(value="₹0.00")
            tk.Label(card, textvariable=value, bg="#ffffff", fg="#1d1d1f", font=("SF Pro Display", 25, "bold")).pack(anchor="w", pady=(8, 0))
            self.overview_cards[key] = value

        chart_panel = tk.Frame(frame, bg="#ffffff", padx=20, pady=18)
        chart_panel.pack(fill="both", expand=True, padx=18, pady=(18, 0))
        tk.Label(chart_panel, text="Spending by category", bg="#ffffff", fg="#1d1d1f", font=("SF Pro Display", 16, "bold")).pack(anchor="w")
        self.chart_canvas = tk.Canvas(chart_panel, bg="#ffffff", highlightthickness=0, height=280)
        self.chart_canvas.pack(fill="both", expand=True, pady=(12, 0))

    def _build_transactions_tab(self):
        frame = tk.Frame(self.content, bg="#f5f5f7")
        self.tabs["transactions"] = frame

        top = tk.Frame(frame, bg="#f5f5f7")
        top.pack(fill="x", padx=18, pady=(18, 10))
        tk.Label(top, text="Transactions", bg="#f5f5f7", fg="#1d1d1f", font=("SF Pro Display", 24, "bold")).pack(side="left")
        tk.Button(top, text="Export CSV", command=self.export_csv, bg="#dfeaff", fg="#111111", relief="flat", bd=0, padx=14, pady=8, font=("SF Pro Display", 10, "bold")).pack(side="right")

        tools = tk.Frame(frame, bg="#f5f5f7")
        tools.pack(fill="x", padx=18, pady=(0, 12))
        self.search_var = tk.StringVar()
        ttk.Entry(tools, textvariable=self.search_var, width=28).pack(side="left")
        tk.Button(tools, text="Search", command=self.refresh_table, bg="#273244", fg="#f7e7b5", relief="flat", bd=0, padx=12, pady=7, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(8, 0))

        form = tk.Frame(frame, bg="#191f2a", padx=16, pady=16)
        form.pack(fill="x", padx=18, pady=(0, 10))
        self.form_vars = {}
        fields = [("Type", "type"), ("Category", "category"), ("Amount", "amount"), ("Note", "note"), ("Date", "date")]
        for label, key in fields:
            row = tk.Frame(form, bg="#191f2a", pady=6)
            row.pack(fill="x")
            tk.Label(row, text=f"{label}:", width=12, bg="#191f2a", fg="#e8dcc3", font=("Segoe UI", 10, "bold")).pack(side="left")
            if key == "type":
                var = tk.StringVar(value="Expense")
                ttk.Combobox(row, textvariable=var, values=["Expense", "Income"], width=25, state="readonly").pack(side="left", fill="x", expand=True)
            else:
                var = tk.StringVar()
                ttk.Entry(row, textvariable=var, width=30).pack(side="left", fill="x", expand=True)
            self.form_vars[key] = var

        actions = tk.Frame(form, bg="#ffffff")
        actions.pack(fill="x", pady=(12, 0))
        tk.Button(actions, text="Save Entry", command=self.add_or_update_transaction, bg="#dfeaff", fg="#111111", relief="flat", bd=0, padx=14, pady=8, font=("SF Pro Display", 10, "bold")).pack(side="left", padx=(0, 10))
        tk.Button(actions, text="Clear", command=self.clear_form, bg="#e5e5ea", fg="#1d1d1f", relief="flat", bd=0, padx=14, pady=8, font=("SF Pro Display", 10, "bold")).pack(side="left")

        self.table = ttk.Treeview(frame, columns=("date", "type", "category", "amount", "note"), show="headings", height=13)
        self.table.heading("date", text="Date")
        self.table.heading("type", text="Type")
        self.table.heading("category", text="Category")
        self.table.heading("amount", text="Amount")
        self.table.heading("note", text="Note")
        self.table.column("date", width=150, anchor="center")
        self.table.column("type", width=90, anchor="center")
        self.table.column("category", width=160, anchor="center")
        self.table.column("amount", width=120, anchor="center")
        self.table.column("note", width=260, anchor="center")
        self.table.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        table_actions = tk.Frame(frame, bg="#f5f5f7")
        table_actions.pack(fill="x", padx=18, pady=(0, 18))
        tk.Button(table_actions, text="Edit Selected", command=self.load_selected_for_edit, bg="#dfeaff", fg="#111111", relief="flat", bd=0, padx=14, pady=8, font=("SF Pro Display", 10, "bold")).pack(side="left", padx=(0, 10))
        tk.Button(table_actions, text="Delete Selected", command=self.delete_selected_transaction, bg="#f3d1d1", fg="#1d1d1f", relief="flat", bd=0, padx=14, pady=8, font=("SF Pro Display", 10, "bold")).pack(side="left")

    def _build_goals_tab(self):
        frame = tk.Frame(self.content, bg="#f5f5f7")
        self.tabs["goals"] = frame

        tk.Label(frame, text="Savings Goals", bg="#f5f5f7", fg="#1d1d1f", font=("SF Pro Display", 24, "bold")).pack(anchor="w", padx=18, pady=(18, 12))

        form = tk.Frame(frame, bg="#ffffff", padx=16, pady=16)
        form.pack(fill="x", padx=18, pady=(0, 10))
        self.goal_vars = {
            "name": tk.StringVar(),
            "target": tk.StringVar(),
            "current": tk.StringVar(),
            "color": tk.StringVar(value="#c8a96b"),
        }

        for label, key in [("Goal Name", "name"), ("Target", "target"), ("Current", "current")]:
            row = tk.Frame(form, bg="#ffffff", pady=6)
            row.pack(fill="x")
            tk.Label(row, text=f"{label}:", width=12, bg="#ffffff", fg="#1d1d1f", font=("SF Pro Display", 10, "bold")).pack(side="left")
            ttk.Entry(row, textvariable=self.goal_vars[key], width=30).pack(side="left", fill="x", expand=True)

        row = tk.Frame(form, bg="#ffffff", pady=6)
        row.pack(fill="x")
        tk.Label(row, text="Color:", width=12, bg="#ffffff", fg="#1d1d1f", font=("SF Pro Display", 10, "bold")).pack(side="left")
        ttk.Combobox(row, textvariable=self.goal_vars["color"], values=["#c8a96b", "#a78bfa", "#10b981", "#f59e0b", "#ef4444"], state="readonly", width=28).pack(side="left")

        actions = tk.Frame(form, bg="#ffffff")
        actions.pack(fill="x", pady=(12, 0))
        tk.Button(actions, text="Add Goal", command=self.add_goal, bg="#dfeaff", fg="#111111", relief="flat", bd=0, padx=14, pady=8, font=("SF Pro Display", 10, "bold")).pack(side="left", padx=(0, 10))
        tk.Button(actions, text="Reset Form", command=self.clear_goal_form, bg="#e5e5ea", fg="#1d1d1f", relief="flat", bd=0, padx=14, pady=8, font=("SF Pro Display", 10, "bold")).pack(side="left")

        self.goals_container = tk.Frame(frame, bg="#f5f5f7")
        self.goals_container.pack(fill="both", expand=True, padx=18, pady=(0, 18))

    def clear_form(self):
        for key in self.form_vars:
            if key == "type":
                self.form_vars[key].set("Expense")
            else:
                self.form_vars[key].set("")

    def clear_goal_form(self):
        self.goal_vars["name"].set("")
        self.goal_vars["target"].set("")
        self.goal_vars["current"].set("")
        self.goal_vars["color"].set("#c8a96b")

    def add_goal(self):
        name = self.goal_vars["name"].get().strip()
        target = self._safe_float(self.goal_vars["target"].get())
        current = self._safe_float(self.goal_vars["current"].get())
        color = self.goal_vars["color"].get() or "#c8a96b"

        if not name or target is None or target <= 0:
            messagebox.showerror("Goal", "Please enter a valid goal name and target value.")
            return
        if current is None:
            current = 0.0

        add_goal(name, target, current, color)
        self.clear_goal_form()
        self.refresh_goals()

    def _safe_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def add_or_update_transaction(self):
        transaction_type = self.form_vars["type"].get().strip()
        category = self.form_vars["category"].get().strip()
        amount = self._safe_float(self.form_vars["amount"].get())
        note = self.form_vars["note"].get().strip()
        date = self.form_vars["date"].get().strip() or None

        if transaction_type not in {"Income", "Expense"}:
            messagebox.showerror("Validation", "Type must be Income or Expense.")
            return
        if not category:
            messagebox.showerror("Validation", "Category is required.")
            return
        if amount is None or amount <= 0:
            messagebox.showerror("Validation", "Amount must be a valid positive number.")
            return

        selected_id = self.table.selection()
        if selected_id:
            index = self.table.index(selected_id[0])
            edit_transaction(index, transaction_type, category, amount, note, date)
            messagebox.showinfo("Updated", "Transaction updated successfully.")
        else:
            add_transaction(transaction_type, category, amount, note, date)
            messagebox.showinfo("Saved", "Transaction added successfully.")

        self.clear_form()
        self.refresh_all()

    def load_selected_for_edit(self):
        selected_id = self.table.selection()
        if not selected_id:
            messagebox.showwarning("Select a row", "Please select a transaction to edit.")
            return

        index = self.table.index(selected_id[0])
        transactions = list_transactions()
        if index >= len(transactions):
            return

        item = transactions[index]
        self.form_vars["type"].set(item.get("type", "Expense"))
        self.form_vars["category"].set(item.get("category", ""))
        self.form_vars["amount"].set(str(item.get("amount", 0)))
        self.form_vars["note"].set(item.get("note", ""))
        self.form_vars["date"].set(item.get("date", ""))

    def delete_selected_transaction(self):
        selected_id = self.table.selection()
        if not selected_id:
            messagebox.showwarning("Remove", "Please select a transaction to delete.")
            return

        if messagebox.askyesno("Delete", "Do you want to delete this transaction?"):
            index = self.table.index(selected_id[0])
            delete_transaction(index)
            self.refresh_all()

    def set_budget(self):
        amount = self._safe_float(self.budget_var.get()) if hasattr(self, "budget_var") else None
        if amount is None or amount < 0:
            messagebox.showerror("Budget", "Please enter a valid budget amount.")
            return
        set_budget(amount)
        self.refresh_summary()

    def refresh_summary(self):
        summary = get_summary()
        self.overview_cards["income"].set(f"₹{summary['income']:.2f}")
        self.overview_cards["expense"].set(f"₹{summary['expense']:.2f}")
        self.overview_cards["balance"].set(f"₹{summary['balance']:.2f}")
        self.overview_cards["budget"].set(f"₹{get_budget():.2f}")
        self.draw_chart(summary["category_totals"])

    def draw_chart(self, category_totals):
        self.chart_canvas.delete("all")
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()
        if width < 10 or height < 10:
            return

        padding = 26
        max_value = max(category_totals.values(), default=1)
        total_bars = max(len(category_totals), 1)
        gap = 18
        bar_width = (width - padding * 2 - gap * (total_bars - 1)) / total_bars
        colors = ["#c8a96b", "#a78bfa", "#10b981", "#f59e0b", "#ef4444", "#9ecae1"]

        for idx, (category, value) in enumerate(category_totals.items()):
            color = colors[idx % len(colors)]
            x0 = padding + idx * (bar_width + gap)
            bar_height = (value / max_value) * (height - 80)
            y0 = height - 40 - bar_height
            self.chart_canvas.create_rectangle(x0, y0, x0 + bar_width, height - 40, fill=color, outline="")
            self.chart_canvas.create_text(x0 + bar_width / 2, height - 18, text=category[:8], fill="#f7e7b5", font=("Segoe UI", 8, "bold"))
            self.chart_canvas.create_text(x0 + bar_width / 2, y0 - 8, text=f"₹{value:.0f}", fill="#fff", font=("Segoe UI", 8, "bold"))

    def refresh_table(self):
        query = self.search_var.get().strip()
        rows = search_transactions(query, "All")
        self.table.delete(*self.table.get_children())
        for item in rows:
            self.table.insert(
                "",
                tk.END,
                values=(
                    item.get("date", ""),
                    item.get("type", ""),
                    item.get("category", ""),
                    f"₹{float(item.get('amount', 0) or 0):.2f}",
                    item.get("note", ""),
                ),
            )

    def refresh_goals(self):
        for child in self.goals_container.winfo_children():
            child.destroy()

        goals = list_goals()
        if not goals:
            tk.Label(self.goals_container, text="No goals created yet.", bg="#f5f5f7", fg="#6e6e73", font=("SF Pro Display", 12)).pack(anchor="w", padx=6, pady=10)
            return

        for goal in goals:
            frame = tk.Frame(self.goals_container, bg="#ffffff", padx=14, pady=12)
            frame.pack(fill="x", pady=8)
            name = goal["name"]
            target = float(goal["target"] or 0)
            current = float(goal["current"] or 0)
            percent = min((current / target) * 100 if target else 0, 100)
            color = goal.get("color", "#c8a96b")

            tk.Label(frame, text=name, bg="#ffffff", fg="#1d1d1f", font=("SF Pro Display", 12, "bold")).pack(anchor="w")
            tk.Label(frame, text=f"₹{current:.2f} / ₹{target:.2f}", bg="#ffffff", fg="#6e6e73", font=("SF Pro Display", 10)).pack(anchor="w", pady=(4, 8))

            bar_bg = tk.Frame(frame, bg="#e5e5ea", height=14)
            bar_bg.pack(fill="x")
            progress = tk.Frame(bar_bg, bg=color, height=14)
            progress.pack(side="left", fill="y")
            progress.configure(width=max(4, int(percent * 2.2)))
            tk.Label(frame, text=f"{percent:.0f}% complete", bg="#ffffff", fg="#1d1d1f", font=("SF Pro Display", 9)).pack(anchor="w", pady=(8, 0))

            actions = tk.Frame(frame, bg="#ffffff")
            actions.pack(anchor="w", pady=(8, 0))
            tk.Button(actions, text="Complete", command=lambda gid=goal["id"], val=target: self.complete_goal(gid, val), bg="#dfeaff", fg="#111111", relief="flat", bd=0, padx=10, pady=6, font=("SF Pro Display", 9, "bold")).pack(side="left", padx=(0, 8))
            tk.Button(actions, text="Delete", command=lambda gid=goal["id"]: self.delete_goal(gid), bg="#f3d1d1", fg="#1d1d1f", relief="flat", bd=0, padx=10, pady=6, font=("SF Pro Display", 9, "bold")).pack(side="left")

    def complete_goal(self, goal_id, target):
        update_goal(goal_id, current=target)
        self.refresh_goals()

    def delete_goal(self, goal_id):
        delete_goal(goal_id)
        self.refresh_goals()

    def refresh_all(self):
        self.refresh_summary()
        self.refresh_table()
        self.refresh_goals()
        self.clear_form()
        self.clear_goal_form()

    def export_csv(self):
        path = Path("expense_report.csv")
        rows = list_transactions()
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "type", "category", "amount", "note"])
            writer.writeheader()
            writer.writerows(rows)
        messagebox.showinfo("Export", f"CSV exported to {path.resolve()}.")


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
