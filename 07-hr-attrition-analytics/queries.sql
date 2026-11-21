-- Load data/hr_data.csv into a table called hr (SQLite: .mode csv / .import data/hr_data.csv hr)

-- 1. Attrition rate by department
SELECT department, COUNT(*) AS employees,
       ROUND(100.0 * SUM(attrition = 'Yes') / COUNT(*), 1) AS attrition_pct
FROM hr GROUP BY department ORDER BY attrition_pct DESC;

-- 2. Roles with above-average attrition (CTE + subquery)
WITH role_rate AS (
    SELECT job_role, COUNT(*) AS employees, 100.0 * SUM(attrition = 'Yes') / COUNT(*) AS attrition_pct
    FROM hr GROUP BY job_role)
SELECT job_role, employees, ROUND(attrition_pct, 1) AS attrition_pct
FROM role_rate
WHERE attrition_pct > (SELECT 100.0 * SUM(attrition = 'Yes') / COUNT(*) FROM hr)
ORDER BY attrition_pct DESC;

-- 3. Overtime vs satisfaction
SELECT overtime, job_satisfaction, COUNT(*) AS employees,
       ROUND(100.0 * SUM(attrition = 'Yes') / COUNT(*), 1) AS attrition_pct
FROM hr GROUP BY overtime, job_satisfaction ORDER BY overtime, job_satisfaction;

-- 4. Rank departments by average income and attrition (window function)
SELECT department, ROUND(AVG(monthly_income)) AS avg_income,
       ROUND(100.0 * SUM(attrition = 'Yes') / COUNT(*), 1) AS attrition_pct,
       RANK() OVER (ORDER BY AVG(monthly_income) DESC) AS income_rank
FROM hr GROUP BY department;
