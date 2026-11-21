"""Run the SQL queries, compute financial KPIs, flag unusual transactions and export for Power BI."""
import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)
con = sqlite3.connect("data/bank.db")
tx = pd.read_sql("SELECT t.*, c.segment, c.region FROM transactions t JOIN customers c USING (customer_id)", con)
tx["txn_date"] = pd.to_datetime(tx["txn_date"])
tx["month"] = tx["txn_date"].dt.to_period("M").dt.to_timestamp()

# ---------- KPIs ----------
income = tx.loc[tx.txn_type == "Income", "amount"].sum()
spend = tx.loc[tx.txn_type == "Expense", "amount"].sum()
kpis = {
    "Total income": income,
    "Total expenditure": spend,
    "Overall savings rate (%)": 100 * (income - spend) / income,
    "Avg monthly spend per customer": spend / tx["customer_id"].nunique() / tx["month"].nunique(),
    "Largest expense category": tx[tx.txn_type == "Expense"].groupby("category")["amount"].sum().idxmax(),
}
for k, v in kpis.items():
    print(f"{k}: {v:,.1f}" if isinstance(v, float) else f"{k}: {v}")
pd.Series(kpis).to_csv("outputs/kpis.csv", header=["value"])

# ---------- Monthly trend ----------
monthly = tx.pivot_table(index="month", columns="txn_type", values="amount", aggfunc="sum")
ax = monthly.plot(figsize=(10, 4.5), color=["#185351", "#c0392b"], marker="o")
ax.set_title("Monthly income vs expenditure"); ax.set_ylabel("GBP")
plt.tight_layout(); plt.savefig("outputs/monthly_income_vs_expenditure.png", dpi=150); plt.close()

# ---------- Category spend ----------
cat = tx[tx.txn_type == "Expense"].groupby("category")["amount"].sum().sort_values()
ax = cat.plot.barh(figsize=(8, 4.5), color="#185351")
ax.set_title("Total spend by category"); ax.set_xlabel("GBP")
plt.tight_layout(); plt.savefig("outputs/spend_by_category.png", dpi=150); plt.close()

# ---------- Unusual transactions (z-score within category) ----------
exp = tx[tx.txn_type == "Expense"].copy()
g = exp.groupby("category")["amount"]
exp["z_score"] = (exp["amount"] - g.transform("mean")) / g.transform("std")
anomalies = exp[exp["z_score"] > 3].sort_values("z_score", ascending=False)
print(f"\nFlagged {len(anomalies)} unusual transactions (z-score > 3 within category)")
print(anomalies[["transaction_id", "customer_id", "category", "amount", "z_score"]].head(10).round(2))
anomalies.to_csv("outputs/unusual_transactions.csv", index=False)

# ---------- Export clean table for Power BI ----------
tx.to_csv("outputs/transactions_for_powerbi.csv", index=False)
print("\nSaved outputs/ (import transactions_for_powerbi.csv into Power BI)")
