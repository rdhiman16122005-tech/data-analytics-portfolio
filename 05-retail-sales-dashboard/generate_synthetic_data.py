"""Create a synthetic retail sales database (SQLite) and CSVs. No real company data."""
import os
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
cats = {
    "Electronics": [("Wireless Headphones", 45, 89), ("Smart Watch", 80, 149), ("Bluetooth Speaker", 28, 59), ("Tablet", 140, 249)],
    "Home": [("Coffee Maker", 25, 54), ("Air Fryer", 40, 95), ("Desk Lamp", 9, 24), ("Vacuum Cleaner", 70, 139)],
    "Fashion": [("Running Shoes", 30, 79), ("Winter Jacket", 45, 119), ("Backpack", 15, 45), ("Sunglasses", 8, 35)],
    "Sports": [("Yoga Mat", 7, 22), ("Dumbbell Set", 25, 59), ("Football", 9, 25), ("Fitness Tracker", 22, 55)],
}
products = pd.DataFrame(
    [(i + 1, name, cat, cost, price)
     for i, (cat, items) in enumerate([(c, p) for c, ps in cats.items() for p in ps])
     for name, cost, price in [items]],
    columns=["product_id", "product_name", "category", "unit_cost", "unit_price"],
)

regions = {"London": 1.5, "South East": 1.2, "North West": 1.0, "Scotland": 0.7, "Wales": 0.5, "Midlands": 0.9}
dates = pd.date_range("2023-01-01", "2025-12-31", freq="D")
n = 30000
order_dates = rng.choice(dates, n)
month_boost = pd.Series(order_dates).dt.month.map(lambda m: 1.6 if m in (11, 12) else 1.0).to_numpy()
keep = rng.random(n) < (month_boost / 1.6)
order_dates = order_dates[keep]
m = len(order_dates)

region = rng.choice(list(regions), m, p=np.array(list(regions.values())) / sum(regions.values()))
sales = pd.DataFrame({
    "order_id": np.arange(1, m + 1),
    "order_date": pd.to_datetime(order_dates).strftime("%Y-%m-%d"),
    "region": region,
    "product_id": rng.choice(products.product_id, m),
    "quantity": rng.choice([1, 2, 3, 4, 5], m, p=[.5, .25, .13, .08, .04]),
    "discount": rng.choice([0, 0.05, 0.10, 0.20], m, p=[.6, .2, .15, .05]),
})

os.makedirs("data", exist_ok=True)
con = sqlite3.connect("data/retail.db")
products.to_sql("products", con, if_exists="replace", index=False)
sales.to_sql("sales", con, if_exists="replace", index=False)
con.close()
products.to_csv("data/products.csv", index=False)
sales.to_csv("data/sales.csv", index=False)
print(f"Created data/retail.db with {len(products)} products and {len(sales)} orders")
