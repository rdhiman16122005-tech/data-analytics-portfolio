-- Retail sales analysis (SQLite syntax)

-- Reusable view: one row per order with revenue and profit
DROP VIEW IF EXISTS v_sales;
CREATE VIEW v_sales AS
SELECT s.order_id, s.order_date,
       substr(s.order_date, 1, 4) AS year,
       substr(s.order_date, 1, 7) AS month,
       s.region, p.category, p.product_name, s.quantity, s.discount,
       s.quantity * p.unit_price * (1 - s.discount)                  AS revenue,
       s.quantity * p.unit_price * (1 - s.discount) - s.quantity * p.unit_cost AS profit
FROM sales s JOIN products p USING (product_id);

-- 1. Revenue, profit and margin by year
SELECT year, ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM v_sales GROUP BY year ORDER BY year;

-- 2. Year-on-year revenue growth (window function)
WITH y AS (SELECT year, SUM(revenue) AS revenue FROM v_sales GROUP BY year)
SELECT year, ROUND(revenue) AS revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY year)) / LAG(revenue) OVER (ORDER BY year), 1) AS yoy_growth_pct
FROM y ORDER BY year;

-- 3. Top 10 best-selling products by revenue
SELECT product_name, category, SUM(quantity) AS units, ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit
FROM v_sales GROUP BY product_name, category ORDER BY revenue DESC LIMIT 10;

-- 4. Most profitable regions
SELECT region, ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM v_sales GROUP BY region ORDER BY profit DESC;

-- 5. Monthly revenue with 3-month moving average
WITH m AS (SELECT month, SUM(revenue) AS revenue FROM v_sales GROUP BY month)
SELECT month, ROUND(revenue) AS revenue,
       ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS moving_avg_3m
FROM m ORDER BY month;

-- 6. Best product in each category (ranking window function)
WITH r AS (
    SELECT category, product_name, SUM(revenue) AS revenue,
           RANK() OVER (PARTITION BY category ORDER BY SUM(revenue) DESC) AS rnk
    FROM v_sales GROUP BY category, product_name)
SELECT category, product_name, ROUND(revenue) AS revenue FROM r WHERE rnk = 1;
