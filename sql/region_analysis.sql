SELECT
Region,
round(sum(Sales),2) as total_sales,
round(sum(Profit),2) as total_profit,
round(sum(Profit)/sum(Sales) , 2) as profit_margin
FROM sales
GROUP BY Region 
ORDER BY total_profit DESC ;
