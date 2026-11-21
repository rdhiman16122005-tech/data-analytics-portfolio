# Power BI build guide

1. **Get Data > Text/CSV** > `outputs/sales_for_powerbi.csv`. In Power Query set `order_date` to *Date*.
2. Create a Date table: `Date = CALENDAR(MIN(sales_for_powerbi[order_date]), MAX(sales_for_powerbi[order_date]))`
   and relate `Date[Date]` to `sales_for_powerbi[order_date]`.
3. Add these **measures**:

```DAX
Total Revenue = SUM(sales_for_powerbi[revenue])
Total Profit  = SUM(sales_for_powerbi[profit])
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
Orders = DISTINCTCOUNT(sales_for_powerbi[order_id])
Avg Order Value = DIVIDE([Total Revenue], [Orders])
Revenue LY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))
Revenue YoY % = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])
```

4. **Visuals:** KPI cards (Revenue, Profit, Margin, Orders) - line chart (revenue by month) -
   clustered column (revenue & profit by year) - bar chart (top 10 products) - map or bar (profit by region) -
   slicers for Year, Region and Category.
5. Publish to Power BI Service and add the link to the README.
