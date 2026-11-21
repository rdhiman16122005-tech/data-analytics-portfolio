# Banking & Financial Data Analysis (SQL, Python, Excel, Power BI)

Analyses transaction patterns, income vs expenditure, and unusual transactions for a retail bank.

## Business question
How do customers earn and spend, where is spending concentrated, and which transactions look unusual?

## Contents
| File | Purpose |
|---|---|
| `generate_synthetic_data.py` | Builds a **synthetic** SQLite database (no real customer data) |
| `queries.sql` | Monthly income vs spend, category share, savings rate by segment, MoM change (window functions), anomaly rule |
| `analysis.py` | Runs KPIs, charts, z-score anomaly flags and exports a CSV for Power BI |

## Run it
```bash
pip install -r requirements.txt
python generate_synthetic_data.py
python analysis.py
sqlite3 data/bank.db < queries.sql      # or open queries.sql in DB Browser for SQLite
```

## Power BI
Import `outputs/transactions_for_powerbi.csv`. Suggested visuals: income vs expenditure line chart,
category spend bar chart, savings-rate by segment, and a table of flagged transactions.

## Findings
_Add your own findings after running on your data._
