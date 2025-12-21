import pandas as pd      # pandas: for data manipulation and analysis (DataFrames)
import numpy as np       # numpy: for numerical operations (arrays, calculations)
import sqlite3           # sqlite3: to connect to SQLite database and execute SQL queries

# STEP 1 - CONNECT TO DB 
DB_File = "sales_analysis.db"

conn = sqlite3.connect(DB_File)

# STEP 2 - READ RAW DATA FROM DB 
# PULL RAW SALES TABLE FROM DB FOR CLEANING AND ANALYSIS 
table_raw = 'sales'
df_raw = pd.read_sql_query(f"SELECT * FROM {table_raw}"  , conn)

# Print shape and sample to verify data has loaded correctly

print(df_raw.shape)
print(df_raw.head())
# STEP 3: INSPECT RAW DATA
# Purpose: Understand the data types, missing values, and basic statistics before cleaning.

# - Data Info -
print(df_raw.info())      # Shows column names, non-null counts, data types
# -- Numeric Summary -
print(df_raw.describe())  # Summary statistics for numeric columns

# STEP 4 - COPY RAW DATA
df = df_raw.copy()

# STEP 5: CLEAN COLUMN NAMES
# -----------------------------
# Purpose: Standardize column names for consistency and ease of use in code.
# Steps:
# - Strip whitespace
# - Convert to lowercase
# - Replace spaces and dashes with underscores
print(df.columns)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" " , "_")
    .str.replace("-","_")
)

print(df.columns.to_list())

# STEP 6: CONVERT DATA TYPES

# Purpose: Ensure each column has the correct type for analysis and calculations.
# Convert 'order_date' and 'ship_date' to datetime

df['order_date'] = pd.to_datetime(df['order_date'],errors='coerce')
df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')

#  Convert numeric columns to float or integer for calculations
numeric_cols = ['row_id', 'sales' , 'profit' , 'discount' , 'quantity']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric , errors='coerce')


# STEP 7: HANDLE MISSING VALUES ( not required as no missing values in dataset)

# Purpose: Clean the data by handling missing or null values, ensuring dataset reliability.
# Drop rows missing critical fields like 'order_date' or 'sales'
# df = df.dropna(subset=['order_date', 'sales'])

# # Fill missing discounts with 0
# df['discount'] = df['discount'].fillna(0)

# # Fill missing profit with median to reduce impact of outliers
# df['profit'] = df['profit'].fillna(df['profit'].median())

# STEP 8: FEATURE ENGINEERING
# Purpose: Create new columns that provide business insights for dashboards and analysis.
# Extract year, month, and month name from order_date

df['order_year'] = df['order_date'].dt.year  #year of order
df['order_month'] = df['order_date'].dt.month #month of the year of the order
df['order_month_name']= df['order_date'].dt.month_name() #month name 
df['profit_margin'] = df['profit']/df['sales']

df['is_profitable'] = np.where(df['profit_margin']>0 , 'Yes' , 'No')

# STEP-9 VALIDATE - CLEANED DATA 

print(df.dtypes)

assert df['sales'].min() >= 0 , "Negetive Sales Detected"
assert df['order_date'].isnull().sum() == 0 , "Missing Order Dates Detected"
print('sample transformed date')
print(df.head)

# STEP 10 -SAVE TRANSFORMED DATA 

table_analytics = 'sales_analysis_python'
df.to_sql(table_analytics,conn, if_exists='replace',index=False)

print('df saved to db')

conn.close()