"""Create a synthetic banking database (SQLite). No real customer data."""
import os
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
n_cust = 400

customers = pd.DataFrame({
    "customer_id": np.arange(1, n_cust + 1),
    "segment": rng.choice(["Student", "Salaried", "Self-employed", "Retired"], n_cust, p=[.15, .55, .2, .1]),
    "region": rng.choice(["London", "South West", "Midlands", "North", "Scotland"], n_cust),
})
base_income = {"Student": 900, "Salaried": 3200, "Self-employed": 2800, "Retired": 1700}

months = pd.period_range("2024-01", "2025-12", freq="M")
expense_cats = {"Rent/Mortgage": .30, "Groceries": .12, "Transport": .07, "Utilities": .05,
                "Dining": .06, "Shopping": .08, "Entertainment": .04, "Travel": .04}
rows = []
tid = 1
for _, c in customers.iterrows():
    inc = base_income[c.segment] * rng.uniform(.8, 1.3)
    for m in months:
        rows.append((tid, c.customer_id, m.to_timestamp().date() + pd.Timedelta(days=int(rng.integers(0, 3))),
                     "Income", "Salary", round(inc * rng.uniform(.97, 1.03), 2))); tid += 1
        for cat, share in expense_cats.items():
            amt = inc * share * rng.uniform(.7, 1.3) * (1.25 if (cat == "Travel" and m.month in (7, 8, 12)) else 1)
            rows.append((tid, c.customer_id,
                         m.to_timestamp().date() + pd.Timedelta(days=int(rng.integers(0, 27))),
                         "Expense", cat, round(amt, 2))); tid += 1

tx = pd.DataFrame(rows, columns=["transaction_id", "customer_id", "txn_date", "txn_type", "category", "amount"])
tx["txn_date"] = pd.to_datetime(tx["txn_date"]).dt.strftime("%Y-%m-%d")

# Inject a few unusual transactions for anomaly detection to find
idx = rng.choice(len(tx[tx.txn_type == "Expense"]), 25, replace=False)
exp_index = tx[tx.txn_type == "Expense"].index[idx]
tx.loc[exp_index, "amount"] = (tx.loc[exp_index, "amount"] * rng.uniform(6, 12, 25)).round(2)

os.makedirs("data", exist_ok=True)
con = sqlite3.connect("data/bank.db")
customers.to_sql("customers", con, if_exists="replace", index=False)
tx.to_sql("transactions", con, if_exists="replace", index=False)
con.close()
print(f"Created data/bank.db: {len(customers)} customers, {len(tx)} transactions")
