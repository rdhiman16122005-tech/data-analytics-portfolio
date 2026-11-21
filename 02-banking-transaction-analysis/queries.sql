-- Banking transaction analysis (SQLite syntax, works in MySQL/PostgreSQL with minor date-function changes)

-- 1. Monthly income vs expenditure and savings rate
WITH monthly AS (
    SELECT substr(txn_date, 1, 7) AS month,
           SUM(CASE WHEN txn_type = 'Income'  THEN amount ELSE 0 END) AS income,
           SUM(CASE WHEN txn_type = 'Expense' THEN amount ELSE 0 END) AS expenditure
    FROM transactions
    GROUP BY month
)
SELECT month, ROUND(income, 0) AS income, ROUND(expenditure, 0) AS expenditure,
       ROUND(100.0 * (income - expenditure) / income, 1) AS savings_rate_pct
FROM monthly
ORDER BY month;

-- 2. Spend by category (share of total expenditure)
SELECT category,
       ROUND(SUM(amount), 0) AS total_spend,
       ROUND(100.0 * SUM(amount) / SUM(SUM(amount)) OVER (), 1) AS share_pct
FROM transactions
WHERE txn_type = 'Expense'
GROUP BY category
ORDER BY total_spend DESC;

-- 3. Savings rate by customer segment
SELECT c.segment,
       ROUND(100.0 * (SUM(CASE WHEN t.txn_type='Income' THEN t.amount END)
                    - SUM(CASE WHEN t.txn_type='Expense' THEN t.amount END))
                    / SUM(CASE WHEN t.txn_type='Income' THEN t.amount END), 1) AS savings_rate_pct
FROM transactions t
JOIN customers c USING (customer_id)
GROUP BY c.segment
ORDER BY savings_rate_pct DESC;

-- 4. Month-on-month expenditure change (window function)
WITH m AS (
    SELECT substr(txn_date,1,7) AS month, SUM(amount) AS spend
    FROM transactions WHERE txn_type='Expense' GROUP BY month
)
SELECT month, ROUND(spend,0) AS spend,
       ROUND(100.0 * (spend - LAG(spend) OVER (ORDER BY month)) / LAG(spend) OVER (ORDER BY month), 1) AS mom_change_pct
FROM m ORDER BY month;

-- 5. Unusual transactions: more than 3x the category average (rule-based flag)
WITH cat_avg AS (
    SELECT category, AVG(amount) AS avg_amt
    FROM transactions WHERE txn_type='Expense' GROUP BY category
)
SELECT t.transaction_id, t.customer_id, t.txn_date, t.category, t.amount,
       ROUND(t.amount / a.avg_amt, 1) AS times_category_avg
FROM transactions t
JOIN cat_avg a USING (category)
WHERE t.txn_type='Expense' AND t.amount > 3 * a.avg_amt
ORDER BY times_category_avg DESC
LIMIT 20;
