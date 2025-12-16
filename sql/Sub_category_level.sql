SELECT

Category,
"Sub-Category",
round(sum(Sales),2) as total_sales,
round(sum(Profit),2) as total_profit,
round(sum(Profit) * 1.0/sum(Sales) , 2) as profit_margin
FROM sales
GROUP BY Category , "Sub-Category"
ORDER BY total_profit  ASC;
