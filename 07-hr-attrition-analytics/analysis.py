"""Employee attrition analysis: where, and why, are people leaving?"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

os.makedirs("outputs", exist_ok=True)
sns.set_theme(style="whitegrid")
df = pd.read_csv("data/hr_data.csv")
df["left"] = (df["attrition"] == "Yes").astype(int)
overall = df["left"].mean()
print(f"Overall attrition: {overall:.1%}\n")

# ---------- 1. Attrition by segment ----------
df["tenure_band"] = pd.cut(df["years_at_company"], [-0.1, 2, 5, 10, 40], labels=["0-2", "2-5", "5-10", "10+"])
df["income_band"] = pd.qcut(df["monthly_income"], 4, labels=["Q1 (low)", "Q2", "Q3", "Q4 (high)"])
cols = ["department", "job_role", "job_satisfaction", "work_life_balance", "overtime", "tenure_band", "income_band"]
tables = {}
for c in cols:
    t = df.groupby(c, observed=True)["left"].agg(employees="count", attrition_rate="mean").round(3)
    tables[c] = t
    print(t, "\n")
pd.concat(tables, names=["factor", "value"]).to_csv("outputs/attrition_by_factor.csv")

fig, ax = plt.subplots(2, 3, figsize=(16, 8))
for a, c in zip(ax.ravel(), ["department", "job_satisfaction", "overtime", "tenure_band", "income_band", "work_life_balance"]):
    t = tables[c].reset_index()
    sns.barplot(data=t, x=c, y="attrition_rate", ax=a, color="#185351")
    a.axhline(overall, ls="--", color="grey"); a.set_title(f"Attrition by {c.replace('_', ' ')}")
    a.tick_params(axis="x", rotation=20); a.set_xlabel("")
    a.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
plt.tight_layout(); plt.savefig("outputs/attrition_by_factor.png", dpi=150); plt.close()

# ---------- 2. Drivers: logistic regression (standardised coefficients) ----------
X = pd.get_dummies(df[["age", "years_at_company", "monthly_income", "job_satisfaction", "work_life_balance",
                       "distance_from_home", "years_since_promotion", "overtime", "department"]], drop_first=True).astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, df["left"], test_size=0.25, random_state=42, stratify=df["left"])
sc = StandardScaler().fit(Xtr)
model = LogisticRegression(max_iter=1000).fit(sc.transform(Xtr), ytr)
print(f"Model ROC-AUC on held-out data: {roc_auc_score(yte, model.predict_proba(sc.transform(Xte))[:, 1]):.3f}")
drivers = pd.DataFrame({"feature": X.columns, "coefficient": model.coef_[0],
                        "odds_ratio_per_1sd": np.exp(model.coef_[0])}).sort_values("coefficient", key=abs, ascending=False)
print(drivers.round(3).head(8))
drivers.to_csv("outputs/attrition_drivers.csv", index=False)

plt.figure(figsize=(8, 5))
d = drivers.head(10).sort_values("coefficient")
plt.barh(d["feature"], d["coefficient"], color=np.where(d["coefficient"] > 0, "#c0392b", "#185351"))
plt.title("Top attrition drivers (red = higher risk of leaving)"); plt.xlabel("Standardised coefficient")
plt.tight_layout(); plt.savefig("outputs/attrition_drivers.png", dpi=150); plt.close()
print("\nSaved outputs/")
