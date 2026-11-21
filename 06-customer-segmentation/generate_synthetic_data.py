"""Synthetic e-commerce order history with different customer behaviours."""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(21)
# (share, orders per year, avg order value, recency tendency in days)
profiles = [(0.15, 14, 90, 20), (0.35, 5, 55, 80), (0.30, 2, 35, 200), (0.20, 1, 25, 300)]
rows, cid, oid = [], 0, 0
end = pd.Timestamp("2025-12-31")
for share, orders_pa, aov, recency in profiles:
    for _ in range(int(2000 * share)):
        cid += 1
        k = max(1, rng.poisson(orders_pa))
        last_gap = int(rng.exponential(recency))
        for _ in range(k):
            oid += 1
            d = end - pd.Timedelta(days=min(364, last_gap + int(rng.integers(0, 365 - min(last_gap, 300)))))
            rows.append((oid, cid, d.strftime("%Y-%m-%d"), round(max(5, rng.normal(aov, aov * 0.3)), 2)))
orders = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "order_value"])
os.makedirs("data", exist_ok=True)
orders.to_csv("data/orders.csv", index=False)
print(f"Saved data/orders.csv: {orders.customer_id.nunique()} customers, {len(orders)} orders")
