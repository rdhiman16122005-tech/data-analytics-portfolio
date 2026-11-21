# Bank Loan Default Analysis (Python)

End-to-end analytics pipeline that identifies default-risk patterns in loan data.

## Business question
Which borrower and loan characteristics are most associated with default?

## What the code does
1. **Cleans** the data: removes duplicates, imputes missing `dti` and employment length.
2. **Engineers features**: loan-to-income ratio, income bands, DTI bands.
3. **Analyses** default rate by grade, DTI band, income band, purpose, home ownership and term.
4. **Visualises** results (Matplotlib / Seaborn) and exports tables to `outputs/`.

## Tools
Python, Pandas, NumPy, Matplotlib, Seaborn

## Run it
```bash
pip install -r requirements.txt
python generate_synthetic_data.py   # creates data/loans.csv (synthetic) - skip if using a real dataset
python analysis.py
```

## Data
`generate_synthetic_data.py` creates **synthetic** data, so no real customer information is used.
To use a real public dataset (e.g. Lending Club on Kaggle), save it as `data/loans.csv` and
rename columns to match, or edit the column names in `analysis.py`.

## Findings
_Add your own findings here after running the analysis on your data (default rate by grade, DTI, etc.)._
