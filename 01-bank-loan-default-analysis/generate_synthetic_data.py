"""Generate a synthetic bank-loan dataset (no real customer data).

Skip this file if you use a real public dataset (e.g. Lending Club on Kaggle):
just save it as data/loans.csv with the same column names, or edit the
column names at the top of analysis.py.
"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 5000

grades = list("ABCDEFG")
grade = rng.choice(grades, n, p=[0.22, 0.28, 0.24, 0.14, 0.07, 0.04, 0.01])
grade_idx = pd.Series(grade).map({g: i for i, g in enumerate(grades)}).to_numpy()

annual_income = rng.lognormal(11.0, 0.5, n).round(-2)
loan_amount = rng.choice(np.arange(2000, 35001, 500), n)
term = rng.choice([36, 60], n, p=[0.7, 0.3])
int_rate = (6 + 2.2 * grade_idx + rng.normal(0, 0.8, n)).clip(5, 30).round(2)
dti = rng.gamma(4, 4.5, n).clip(0, 40).round(1)
emp_length = rng.integers(0, 11, n).astype(float)
home = rng.choice(["RENT", "MORTGAGE", "OWN"], n, p=[0.45, 0.42, 0.13])
purpose = rng.choice(
    ["debt_consolidation", "credit_card", "home_improvement", "car", "small_business", "other"],
    n, p=[0.45, 0.22, 0.10, 0.07, 0.06, 0.10],
)

logit = (-3.6 + 0.30 * grade_idx + 0.035 * dti - 0.000006 * annual_income
         + 0.00002 * loan_amount + 0.25 * (term == 60))
p_default = 1 / (1 + np.exp(-logit))
status = np.where(rng.random(n) < p_default, "Charged Off", "Fully Paid")

df = pd.DataFrame({
    "loan_id": np.arange(1, n + 1),
    "loan_amount": loan_amount, "term_months": term, "int_rate": int_rate,
    "grade": grade, "annual_income": annual_income, "dti": dti,
    "emp_length_years": emp_length, "home_ownership": home,
    "purpose": purpose, "loan_status": status,
})

# Inject realistic missing values so the cleaning step has something to do
df.loc[rng.choice(n, 250, replace=False), "emp_length_years"] = np.nan
df.loc[rng.choice(n, 100, replace=False), "dti"] = np.nan

os.makedirs("data", exist_ok=True)
df.to_csv("data/loans.csv", index=False)
print(f"Saved data/loans.csv  ({len(df)} rows)")
