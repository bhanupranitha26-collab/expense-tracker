# Expense Tracker (Python + CSV)

A simple console-based Expense Tracker built with Python.
Data is stored in a CSV file (`expenses.csv`). The app supports:
- Add expense (id auto-increment)
- View all expenses
- Show total expenses (all time)
- Show monthly totals
- Show category-wise totals
- Delete expense by id
- Export backup CSV

## Tech
- Python 3
- CSV file for persistence

## How to run
1. Clone or download the repo.
2. (Optional) Install tabulate for prettier tables:
   `pip install tabulate`
3. Run:
   `python expense_tracker.py`

## File structure
- `expense_tracker.py` - main program
- `expenses.csv` - data (created automatically if missing)

## Notes
- Date format accepted: `YYYY-MM-DD`, `DD-MM-YYYY`, or `DD/MM/YYYY`.
- Monthly summary accepts `YYYY-MM` or `MM-YYYY`.
