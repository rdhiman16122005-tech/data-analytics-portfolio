# Customer Segmentation & Behaviour Analysis (Python, Pandas, SQL, Power BI)

## Business question
Who are our frequent and occasional customers, and how should marketing treat each group?

## Method
1. Build **RFM** features (Recency, Frequency, Monetary) from order history with Pandas.
2. Log-transform and scale; choose the number of segments using the **silhouette score**.
3. Segment with **K-Means**, profile each segment, and attach a recommended marketing action.

## Run it
```bash
pip install -r requirements.txt
python generate_synthetic_data.py     # synthetic orders - or use your own data/orders.csv
python segmentation.py
```
`data/orders.csv` needs: `order_id, customer_id, order_date, order_value`.
Load `outputs/customers_with_segments.csv` into Power BI for a segment dashboard.

## Findings
_Add your own findings (segment sizes, revenue share, recommended actions) after running._
