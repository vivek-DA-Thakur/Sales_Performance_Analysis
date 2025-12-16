SELECT
strftime('%Y-%m', date(
substr("Order Date", -4) || '-' ||
printf('%02d',substr("Order Date", 1 , instr("Order Date" , '/') -1)) || '-' ||
printf('%02d',substr("Order Date" , instr("Order Date", '/') + 1 , instr(substr("Order Date", instr("Order Date",'/') + 1) , '/') - 1)
)
)
) as month,
Category,
round(sum(Sales),2) as total_sales,
round(sum(Profit),2) as total_profit
FROM sales
GROUP BY month , Category
ORDER BY month , total_profit DESC ;