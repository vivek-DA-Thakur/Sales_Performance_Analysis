SELECT 
ROUND(SUM(Sales) , 2) AS total_sales , 
ROUND(SUM(Profit) , 2) AS total_profit,
round(sum(Profit)/sum(Sales),2) as "Profit Margin" 
FROM sales ;