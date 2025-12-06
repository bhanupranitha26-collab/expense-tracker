#!/usr/bin/env python3
"""
Expense Tracker (CSV-based)
Features:
- Add expense (id auto-increment)
- View all expenses
- Show total expenses
- Show monthly total
- Show category-wise totals
- Delete expense by id
- Export CSV backup
"""

import csv
import os
import shutil
from datetime import datetime

# Optional pretty table
try:
    from tabulate import tabulate
    USE_TABULATE = True
except Exception:
    USE_TABULATE = False

DATA_FILE = "expenses.csv"
FIELDNAMES = ["id", "date", "amount", "category", "note"]  # date in YYYY-MM-DD


def ensure_datafile():
    """Create CSV with header if missing."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_all_expenses():
    ensure_datafile()
    with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_all_expenses(expenses):
    with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for e in expenses:
            writer.writerow(e)


def next_id(expenses):
    if not expenses:
        return "1"
    ids = [int(e["id"]) for e in expenses if e["id"].isdigit()]
    return str(max(ids) + 1)


def parse_date(s):
    """Parse date string in YYYY-MM-DD (or try common formats). Returns date object or None."""
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def input_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty.")


def pretty_print_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return
    rows = [[e["id"], e["date"], e["amount"], e["category"], e["note"]] for e in expenses]
    headers = ["id", "date", "amount", "category", "note"]
    if USE_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        return
    # fallback
    col_widths = [max(len(h), max(len(str(r[i])) for r in rows)) for i, h in enumerate(headers)]
    header = " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers)))
    sep = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    print(header)
    print(sep)
    for r in rows:
        print(" | ".join(str(r[i]).ljust(col_widths[i]) for i in range(len(r))))


def add_expense():
    expenses = read_all_expenses()
    date_str = input_nonempty("Enter date (YYYY-MM-DD) [leave blank for today]: ")
    if not date_str:
        date_obj = datetime.now().date()
        date_str = date_obj.strftime("%Y-%m-%d")
    else:
        date_obj = parse_date(date_str)
        if not date_obj:
            print("Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY.")
            return
        date_str = date_obj.strftime("%Y-%m-%d")
    amt_str = input_nonempty("Enter amount (numbers only): ")
    try:
        amount = float(amt_str)
    except ValueError:
        print("Invalid amount.")
        return
    category = input_nonempty("Enter category (e.g., food, transport, shopping): ").lower()
    note = input("Enter note (optional): ").strip()
    eid = next_id(expenses)
    entry = {
        "id": eid,
        "date": date_str,
        "amount": f"{amount:.2f}",
        "category": category,
        "note": note,
    }
    expenses.append(entry)
    write_all_expenses(expenses)
    print("Expense added.")


def view_expenses():
    expenses = read_all_expenses()
    # sort by date descending
    try:
        expenses.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    except Exception:
        pass
    pretty_print_expenses(expenses)


def total_expenses():
    expenses = read_all_expenses()
    total = sum(float(e["amount"]) for e in expenses) if expenses else 0.0
    print(f"Total expenses: ₹{total:.2f}")


def monthly_total():
    m = input_nonempty("Enter month (YYYY-MM) or (MM-YYYY) : ")
    # normalize to YYYY-MM
    mm = None
    try:
        if "-" in m:
            parts = m.split("-")
            if len(parts[0]) == 4:  # YYYY-MM
                mm = m
            else:  # maybe MM-YYYY
                mm = f"{parts[1]}-{parts[0].zfill(2)}"
        else:
            print("Invalid format. Use YYYY-MM or MM-YYYY.")
            return
    except Exception:
        print("Invalid month format.")
        return
    expenses = read_all_expenses()
    total = 0.0
    for e in expenses:
        if e["date"].startswith(mm):
            total += float(e["amount"])
    print(f"Total for {mm}: ₹{total:.2f}")


def category_totals():
    expenses = read_all_expenses()
    totals = {}
    for e in expenses:
        cat = e["category"].lower()
        totals[cat] = totals.get(cat, 0.0) + float(e["amount"])
    if not totals:
        print("No expenses.")
        return
    rows = [[cat, f"{amt:.2f}"] for cat, amt in totals.items()]
    if USE_TABULATE:
        print(tabulate(rows, headers=["category", "total"], tablefmt="grid"))
        return
    for cat, amt in rows:
        print(f"{cat}: ₹{amt}")


def delete_expense():
    eid = input_nonempty("Enter expense id to delete: ")
    expenses = read_all_expenses()
    found = False
    for e in expenses:
        if e["id"] == eid:
            found = True
            print("Found expense:")
            print(e)
            confirm = input("Delete? (y/N): ").strip().lower()
            if confirm == "y":
                expenses = [x for x in expenses if x["id"] != eid]
                write_all_expenses(expenses)
                print("Deleted.")
            else:
                print("Cancelled.")
            break
    if not found:
        print("Expense id not found.")


def export_backup():
    ensure_datafile()
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(backup_dir, f"expenses_backup_{ts}.csv")
    shutil.copy2(DATA_FILE, dst)
    print(f"Backup created: {dst}")


def menu():
    options = {
        "1": ("Add expense", add_expense),
        "2": ("View all expenses", view_expenses),
        "3": ("Total expenses (all time)", total_expenses),
        "4": ("Monthly total", monthly_total),
        "5": ("Category-wise totals", category_totals),
        "6": ("Delete expense by id", delete_expense),
        "7": ("Export CSV backup", export_backup),
        "8": ("Exit", None),
    }
    while True:
        print("\n----- Expense Tracker -----")
        for k, v in options.items():
            print(f"{k}. {v[0]}")
        choice = input("Choose an option: ").strip()
        if choice not in options:
            print("Invalid choice.")
            continue
        if choice == "8":
            print("Goodbye!")
            break
        try:
            options[choice][1]()
        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nExiting... bye!")
