"""Synthetic HR dataset (no real employee data) with realistic attrition drivers."""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(5)
n = 3000
dept = rng.choice(["Sales", "Research & Development", "Human Resources", "Finance", "IT"], n, p=[.28, .32, .08, .14, .18])
roles = {"Sales": ["Sales Executive", "Sales Manager"], "Research & Development": ["Research Scientist", "Lab Technician"],
         "Human Resources": ["HR Specialist"], "Finance": ["Financial Analyst", "Accountant"], "IT": ["Developer", "Data Analyst"]}
job_role = [rng.choice(roles[d]) for d in dept]
age = rng.integers(21, 60, n)
years_at_company = np.clip(rng.gamma(2.2, 3.0, n), 0, 35).round(1)
monthly_income = (2200 + 90 * years_at_company + rng.normal(0, 700, n) + (age - 21) * 30).clip(1800, 12000).round(-1)
satisfaction = rng.integers(1, 5, n)
work_life = rng.integers(1, 5, n)
overtime = rng.choice(["Yes", "No"], n, p=[.3, .7])
distance = rng.integers(1, 30, n)
promo_gap = np.clip(rng.gamma(1.5, 1.5, n), 0, 12).round(1)

logit = (-2.6 - 0.55 * (satisfaction - 2.5) - 0.35 * (work_life - 2.5) + 1.0 * (overtime == "Yes")
         - 0.00018 * (monthly_income - 5000) - 0.05 * years_at_company + 0.015 * distance
         + 0.08 * promo_gap + 0.35 * (dept == "Sales"))
attrition = np.where(rng.random(n) < 1 / (1 + np.exp(-logit)), "Yes", "No")

df = pd.DataFrame({"employee_id": np.arange(1, n + 1), "department": dept, "job_role": job_role, "age": age,
                   "years_at_company": years_at_company, "monthly_income": monthly_income,
                   "job_satisfaction": satisfaction, "work_life_balance": work_life, "overtime": overtime,
                   "distance_from_home": distance, "years_since_promotion": promo_gap, "attrition": attrition})
os.makedirs("data", exist_ok=True)
df.to_csv("data/hr_data.csv", index=False)
print(f"Saved data/hr_data.csv ({len(df)} employees, attrition rate {(df.attrition=='Yes').mean():.1%})")
