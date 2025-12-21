import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

# connecting to db 

# open communication to sqlite db 

conn = sqlite3.connect('sales_analysis.db')

# loading data into python - run sql and load result into dataframe(df)

df = pd.read_sql_query("SELECT * FROM sales", conn)

#sql is done now py takes over

# understanding date - converting text date to real time date object

df['Order Date'] = pd.to_datetime(
    df['Order Date']
)

#now py knows year month and date 

# creating month buckets 

df['YearMonth'] = df['Order Date'].dt.to_period('M')

# create visuals folder if not present

if not os.path.exists('visuals'):
    os.makedirs('visuals')

# visual 1 - Regional sales profit

region_summary = (
    df
    .groupby('Region')
    .agg({'Sales':'sum' , 'Profit' : 'sum'})
    .reset_index()
)

plt.figure(figsize=(8,5))

sns.barplot(
    x='Region',
    y='Sales',
    data=region_summary,
    color='orange',
    label='Sales'

)

sns.barplot(
    x='Region',
    y='Profit',
    data=region_summary,
    color='orange',
    label='Profit'
)

plt.title('Regional Sales and Profit')
plt.ylabel('Amount')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/region_analysis.png')
plt.close()

#visual2 Sub Category Profit leakage

category_summary = (
    df
    .groupby(['Category', 'Sub-Category'])
    .agg({'Profit': 'sum'})
    .reset_index()
)

plt.figure(figsize=(10, 6))
sns.barplot(
    x='Profit',
    y='Sub-Category',
    hue='Category',
    data=category_summary
)

plt.title('Sub-Category Profit by Category')
plt.tight_layout()
plt.savefig('visuals/category_profit_chart.png')
plt.close()


# VISUAL 3 — Monthly Trend

monthly_summary = (
    df
    .groupby('YearMonth')
    .agg({'Sales': 'sum', 'Profit': 'sum'})
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.plot(
    monthly_summary['YearMonth'].astype(str),
    monthly_summary['Sales'],
    label='Sales',
    marker='o'
)
plt.plot(
    monthly_summary['YearMonth'].astype(str),
    monthly_summary['Profit'],
    label='Profit',
    marker='o'
)

plt.xticks(rotation=45)
plt.title('Monthly Sales & Profit')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/monthly_trends.png')
plt.close()

#  VISUAL 4 — Profit Margin Heatmap

df['Profit_Margin'] = df['Profit'] / df['Sales']

heatmap_data = df.pivot_table(
    index='Category',
    columns='YearMonth',
    values='Profit_Margin',
    aggfunc='mean'
)

plt.figure(figsize=(12, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap='YlGnBu'
)

plt.title('Profit Margin Heatmap by Category & Month')
plt.tight_layout()
plt.savefig('visuals/profit_margin_heatmap.png')
plt.close()


