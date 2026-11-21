"""Bank loan default analysis: cleaning, feature engineering, EDA and key drivers."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("outputs", exist_ok=True)
sns.set_theme(style="whitegrid")

# ---------- 1. Load ----------
df = pd.read_csv("data/loans.csv")
print("Rows:", len(df))
print("Missing values:\n", df.isna().sum()[df.isna().sum() > 0], "\n")

# ---------- 2. Clean ----------
df = df.drop_duplicates("loan_id")
df["emp_length_years"] = df["emp_length_years"].fillna(df["emp_length_years"].median())
df["dti"] = df["dti"].fillna(df.groupby("grade")["dti"].transform("median"))
df["default"] = (df["loan_status"] == "Charged Off").astype(int)

# ---------- 3. Feature engineering ----------
df["loan_to_income"] = df["loan_amount"] / df["annual_income"]
df["income_band"] = pd.qcut(df["annual_income"], 4, labels=["Q1 (low)", "Q2", "Q3", "Q4 (high)"])
df["dti_band"] = pd.cut(df["dti"], [0, 10, 20, 30, 100], labels=["0-10", "10-20", "20-30", "30+"])

# ---------- 4. Default rate by segment ----------
overall = df["default"].mean()
print(f"Overall default rate: {overall:.1%}\n")

summaries = {}
for col in ["grade", "dti_band", "income_band", "purpose", "home_ownership", "term_months"]:
    t = (df.groupby(col, observed=True)["default"]
           .agg(loans="count", default_rate="mean").round(3))
    summaries[col] = t
    print(t, "\n")
pd.concat(summaries, names=["segment", "value"]).to_csv("outputs/default_rate_by_segment.csv")

# ---------- 5. Charts ----------
fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
for ax, col in zip(axes, ["grade", "dti_band", "income_band"]):
    t = summaries[col].reset_index()
    sns.barplot(data=t, x=col, y="default_rate", ax=ax, color="#185351")
    ax.axhline(overall, ls="--", color="grey", label="Overall")
    ax.set_title(f"Default rate by {col.replace('_', ' ')}")
    ax.set_ylabel("Default rate")
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
axes[0].legend()
plt.tight_layout()
plt.savefig("outputs/default_rate_by_segment.png", dpi=150)
plt.close()

num_cols = ["loan_amount", "int_rate", "annual_income", "dti", "emp_length_years",
            "loan_to_income", "default"]
plt.figure(figsize=(7, 5.5))
sns.heatmap(df[num_cols].corr(), annot=True, fmt=".2f", cmap="RdBu_r", center=0)
plt.title("Correlation matrix")
plt.tight_layout()
plt.savefig("outputs/correlation_heatmap.png", dpi=150)
plt.close()

# ---------- 6. Which features are most associated with default? ----------
corr = df[num_cols].corr()["default"].drop("default").sort_values(key=abs, ascending=False)
print("Correlation with default:\n", corr.round(3))
corr.to_csv("outputs/correlation_with_default.csv")
print("\nCharts and tables saved to outputs/")
