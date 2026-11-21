# Retail Sales Performance & Revenue Analytics Dashboard (SQL, Excel, Power BI)

## Business question
How is the retail business performing, which products and regions drive profit, and how do sales trend over time?

## Contents
- `generate_synthetic_data.py` - builds a **synthetic** retail database (no real company data)
- `sql/queries.sql` - revenue/profit by year, YoY growth, top products, regional profit, moving average, ranking
- `analysis.py` - KPIs, charts, and a flat CSV for the dashboard
- `powerbi_dax_measures.md` - step-by-step Power BI build and DAX measures

## Run it
```bash
pip install -r requirements.txt
python generate_synthetic_data.py
python analysis.py
sqlite3 data/retail.db < sql/queries.sql
```
Then follow `powerbi_dax_measures.md`. Add a screenshot of your dashboard (`/images`) and the Power BI link here.

## Findings
_Add your own findings after building the dashboard._
