import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# 1. LOAD SEMUA DATA YANG DIBUTUHKAN
orders = pd.read_csv('olist_orders_dataset.csv')
items = pd.read_csv('olist_order_items_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')

df = pd.merge(items, orders, on='order_id')
df = pd.merge(df, customers, on='customer_id')

# 2. DATA PREPARATION (UTAMA)
df = pd.merge(items, orders, on='order_id')
df['Total_Sales'] = df['price'] + df['freight_value'] 
df['Order_Date'] = pd.to_datetime(df['order_purchase_timestamp'])

# --- BAGIAN 1: SCATTER PLOT (Harga vs Volume) ---
product_analysis = df.groupby('product_id').agg({
    'price': 'mean',
    'order_id': 'count'
}).rename(columns={'price': 'Price_Per_Unit', 'order_id': 'Quantity'})

plt.figure(figsize=(10, 5))
sns.scatterplot(data=product_analysis, x='Price_Per_Unit', y='Quantity', alpha=0.5)
plt.axvline(product_analysis['Price_Per_Unit'].mean(), color='red', linestyle='--')
plt.axhline(product_analysis['Quantity'].mean(), color='green', linestyle='--')
plt.title('Scatter Plot: Harga vs Volume Penjualan')
plt.show()

# --- BAGIAN 2: RFM ANALYSIS (Segmentasi Pelanggan) ---
df_rfm_all = pd.merge(df, customers, on='customer_id')
snapshot_date = df_rfm_all['Order_Date'].max() + pd.Timedelta(days=1)

rfm = df_rfm_all.groupby('customer_unique_id').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'nunique',
    'Total_Sales': 'sum'
})
rfm.columns = ['Recency', 'Frequency', 'Monetary']

plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1); sns.histplot(rfm['Recency'], kde=True, color='blue'); plt.title('Recency (Hari)')
plt.subplot(1, 3, 2); sns.histplot(rfm['Frequency'], kde=True, color='green'); plt.title('Frequency (Order)')
plt.subplot(1, 3, 3); sns.histplot(rfm['Monetary'], kde=True, color='red'); plt.title('Monetary (Nilai)')
plt.tight_layout()
plt.show()

# --- BAGIAN 3: ANALISIS KONTRIBUSI KATEGORI (Efisiensi) ---
df_cat = pd.merge(df, products, on='product_id')
category_analysis = df_cat.groupby('product_category_name').agg({
    'Total_Sales': 'sum',
    'freight_value': 'sum'
}).reset_index()

category_analysis['Efficiency'] = category_analysis['Total_Sales'] / category_analysis['freight_value']
# Urutkan 10 terbawah (paling tidak efisien)
worst_categories = category_analysis.sort_values(by='Efficiency', ascending=True).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=worst_categories, x='Efficiency', y='product_category_name', palette='Reds_r')
plt.title('Top 10 Kategori Paling Tidak Efisien')
plt.show()

# --- BAGIAN 4: UJI HIPOTESIS SEDERHANA ---
median_budget = df['freight_value'].median()
high_budget = df[df['freight_value'] > median_budget]['Total_Sales']
low_budget = df[df['freight_value'] <= median_budget]['Total_Sales']

print(f"\n--- HASIL ANALISIS ---")
print(f"Rerata Sales (Budget Tinggi): {high_budget.mean():.2f}")
print(f"Rerata Sales (Budget Rendah): {low_budget.mean():.2f}")
print("\nAnalisis Selesai!")

     
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# 1. LOAD DATA
items = pd.read_csv('olist_order_items_dataset.csv')
orders = pd.read_csv('olist_orders_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv') # File sumber customer_unique_id

# 2. MERGING 
df = pd.merge(items, orders, on='order_id')

# Langkah B: Gabung dengan data customer (Di sini customer_unique_id dimasukkan ke df)
df = pd.merge(df, customers, on='customer_id')

# 3. PREPARATION
df['Order_Date'] = pd.to_datetime(df['order_purchase_timestamp'])
df['Total_Sales'] = df['price'] + df['freight_value']

# 4. RFM ANALYSIS & SCORING
snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

# Sekarang baris ini tidak akan error karena customer_unique_id sudah ada di df
rfm = df.groupby('customer_unique_id').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'order_id': 'nunique',
    'Total_Sales': 'sum'
})

# Rename kolom agar rapi
rfm.columns = ['Recency', 'Frequency', 'Monetary']

# TAMBAHKAN SCORING 
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['RFM_Group'] = rfm.R_Score.astype(str) + rfm.F_Score.astype(str) + rfm.M_Score.astype(str)

print("--- DATA RFM BERHASIL DIHITUNG ---")
print(rfm.head())

df['Ad_Budget'] = df['freight_value'] 
df['Total_Sales'] = df['price'] + df['freight_value']

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X = df[['Ad_Budget']] # Fitur
y = df['Total_Sales'] # Target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print(f"Koefisien Iklan: {model.coef_[0]}")
print(f"Akurasi Model (R2 Score): {model.score(X_test, y_test)}")
