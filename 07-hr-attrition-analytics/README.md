# HR Analytics & Employee Attrition (Excel, Python, SQL, Power BI)

## Business question
Why are employees leaving, which groups are most affected, and what can the company do about it?

## Method
- Attrition rate by department, role, satisfaction, overtime, tenure and income band
- Logistic regression on standardised features to rank attrition drivers (ROC-AUC reported on held-out data)
- SQL queries (`queries.sql`) for the same questions using GROUP BY, CTEs, subqueries and window functions

## Run it
```bash
pip install -r requirements.txt
python generate_synthetic_data.py     # synthetic HR data - or use your own data/hr_data.csv
python analysis.py
```
Use `outputs/attrition_by_factor.csv` in Excel / Power BI for the dashboard.

## Recommendations
_Add retention recommendations based on your own findings (e.g. overtime policy, promotion pathways)._
