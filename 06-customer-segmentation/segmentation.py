"""RFM customer segmentation with K-Means, segment profiling and marketing recommendations."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

os.makedirs("outputs", exist_ok=True)
orders = pd.read_csv("data/orders.csv", parse_dates=["order_date"])

# ---------- 1. RFM features ----------
snapshot = orders["order_date"].max() + pd.Timedelta(days=1)
rfm = orders.groupby("customer_id").agg(
    recency=("order_date", lambda s: (snapshot - s.max()).days),
    frequency=("order_id", "count"),
    monetary=("order_value", "sum"),
).reset_index()
rfm["avg_order_value"] = rfm["monetary"] / rfm["frequency"]

# ---------- 2. Scale (log to reduce skew) and choose k ----------
X = StandardScaler().fit_transform(np.log1p(rfm[["recency", "frequency", "monetary"]]))
scores = {}
for k in range(2, 8):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    scores[k] = silhouette_score(X, km.labels_)
print("Silhouette score by k:", {k: round(v, 3) for k, v in scores.items()})
best_k = 4   # business-friendly; check the silhouette scores above and adjust if you prefer
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(list(scores), list(scores.values()), "o-", color="#185351")
ax.set_xlabel("k"); ax.set_ylabel("Silhouette score"); ax.set_title("Choosing the number of segments")
plt.tight_layout(); plt.savefig("outputs/silhouette_by_k.png", dpi=150); plt.close()

# ---------- 3. Final clustering ----------
rfm["cluster"] = KMeans(n_clusters=best_k, n_init=10, random_state=42).fit_predict(X)
profile = rfm.groupby("cluster").agg(
    customers=("customer_id", "count"), recency=("recency", "mean"),
    frequency=("frequency", "mean"), monetary=("monetary", "mean"),
    avg_order_value=("avg_order_value", "mean")).round(1)

# ---------- 4. Name segments from their behaviour ----------
order = profile.sort_values(["frequency", "monetary"], ascending=False).index.tolist()
names = ["Champions", "Loyal customers", "At risk / occasional", "Lost / one-off"] + [f"Segment {i}" for i in range(5, 12)]
label = {c: names[i] for i, c in enumerate(order)}
rfm["segment"] = rfm["cluster"].map(label)
profile["segment"] = profile.index.map(label)
profile["revenue_share_pct"] = (100 * profile["monetary"] * profile["customers"]
                                / (profile["monetary"] * profile["customers"]).sum()).round(1)
print(profile.sort_values("monetary", ascending=False), "\n")

actions = {
    "Champions": "Reward with loyalty perks, early access and referral incentives.",
    "Loyal customers": "Cross-sell and upsell, bundle offers, encourage reviews.",
    "At risk / occasional": "Win-back emails and time-limited discounts before they lapse.",
    "Lost / one-off": "Low-cost reactivation campaign, survey to learn why they left.",
}
profile["recommended_action"] = profile["segment"].map(actions).fillna("Test targeted offers.")
profile.to_csv("outputs/segment_profile.csv")
rfm.to_csv("outputs/customers_with_segments.csv", index=False)

# ---------- 5. Charts ----------
fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
for a, col in zip(ax, ["recency", "frequency", "monetary"]):
    sns.boxplot(data=rfm, x="segment", y=col, ax=a, color="#9bc4c1")
    a.set_title(col.capitalize()); a.tick_params(axis="x", rotation=25); a.set_xlabel("")
plt.tight_layout(); plt.savefig("outputs/rfm_by_segment.png", dpi=150); plt.close()
print("Saved outputs/")
