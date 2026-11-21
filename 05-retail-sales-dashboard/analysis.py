"""Sales KPIs, charts, and a clean table for the Power BI dashboard."""
import os
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("outputs", exist_ok=True)
con = sqlite3.connect("data/retail.db")
con.executescript(open("sql/queries.sql").read().split("-- 1.")[0])   # create v_sales view
df = pd.read_sql("SELECT * FROM v_sales", con)
df["order_date"] = pd.to_datetime(df["order_date"])

print(f"Total revenue: {df.revenue.sum():,.0f}")
print(f"Total profit : {df.profit.sum():,.0f}  (margin {100*df.profit.sum()/df.revenue.sum():.1f}%)")
print(f"Orders       : {len(df):,}   Avg order value: {df.revenue.mean():,.2f}\n")

yearly = df.groupby("year")[["revenue", "profit"]].sum()
yearly["yoy_growth_pct"] = yearly["revenue"].pct_change() * 100
print(yearly.round(1), "\n")

top = df.groupby("product_name")[["revenue", "profit"]].sum().sort_values("revenue", ascending=False).head(10)
region = df.groupby("region")[["revenue", "profit"]].sum().sort_values("profit", ascending=False)
monthly = df.groupby(df["order_date"].dt.to_period("M").dt.to_timestamp())["revenue"].sum()

fig, ax = plt.subplots(2, 2, figsize=(14, 9))
monthly.plot(ax=ax[0, 0], color="#185351"); ax[0, 0].set_title("Monthly revenue")
yearly[["revenue", "profit"]].plot.bar(ax=ax[0, 1], color=["#185351", "#e0a526"]); ax[0, 1].set_title("Revenue and profit by year")
top["revenue"].sort_values().plot.barh(ax=ax[1, 0], color="#185351"); ax[1, 0].set_title("Top 10 products by revenue")
region["profit"].plot.bar(ax=ax[1, 1], color="#185351"); ax[1, 1].set_title("Profit by region")
plt.tight_layout(); plt.savefig("outputs/sales_overview.png", dpi=150); plt.close()

# Clean flat table: load this file into Power BI
df.to_csv("outputs/sales_for_powerbi.csv", index=False)
top.to_csv("outputs/top_products.csv"); region.to_csv("outputs/region_performance.csv")
print("Saved outputs/ (import sales_for_powerbi.csv into Power BI)")
