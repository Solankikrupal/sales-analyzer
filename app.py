import pandas as pd

myvar = pd.read_excel('Updated-Product-Sales-Region.xlsx')
myvar = myvar.loc[:, ~myvar.columns.str.contains('^Unnamed')]

# # List the columns you want to convert
date_cols = ['Date', 'OrderDate', 'DeliveryDate']

# myvar.fillna({'Promotion':'NOPROMOTION'},inplace= True);

# myvar['Revenue (Gross)'] = myvar['Quantity']*myvar['UnitPrice'];

# # Loop through the list and convert each one
# for col in date_cols:
#     myvar[col] = pd.to_datetime(myvar[col], format='mixed', errors='coerce');
# # myvar.drop('Unnamed: 0.1', axis=1, inplace=True)

# myvar.to_excel('Updated-Product-Sales-Region.xlsx',index=False);

# print(myvar.duplicated().to_string())

# print(myvar.to_string())
# print( myvar.corr(numeric_only=True) )
# myvar.drop('Unnamed: 0')
# myvar.fillna(0);
# myvar.drop_duplicates();
# print(myvar.describe());


# print(myvar.info())      # Check data types
# print(myvar.describe())  # Get statistical summary

#LEVEL 1 — BASIC (Must Do)

# Revenue & Orders

# Total Revenue (Gross)
def total_gross_revenue(file):
    return file['Revenue (Gross)'].sum();

print("Total Revenue : ", total_gross_revenue(myvar));

# Total Orders (count of OrderID)
def total_order_count(file):
    return file.OrderID.count();

print("Total Order Count : ", total_order_count(myvar));

#Average Order Value
def avg_order_value(file):
    return file.TotalPrice.mean();

print("Avg Order Value : ",avg_order_value(myvar));

#Product Insights

#Top-selling products (by Revenue)
def top_selling_products_by_revenue(file):
    print('Top-selling products (by Revenue)');
    return file.groupby('Product')['Revenue (Gross)'].sum().sort_values(ascending=False).head();

print(top_selling_products_by_revenue(myvar))

#Most sold products (by Quantity)
def most_sold_products_by_qty(file):
    print('Most sold products (by Quantity)')
    return file.groupby('Product')['Quantity'].sum().sort_values(ascending=False);

print(most_sold_products_by_qty(myvar));

#Least performing products
def least_perfoming_products(file):
    print('Least performing products')
    return file.groupby('Product')['Revenue (Gross)'].sum().sort_values(ascending=True).head();

print(least_perfoming_products(myvar));

# Region Insights

# Revenue by Region
def revenue_by_region(file):
    print('Revenue by Region');
    return file.groupby('Region')['Revenue (Gross)'].sum().sort_values(ascending=False);

print(revenue_by_region(myvar));

#Orders by Region
def orders_by_region(file):
    print('Orders by Region')
    return file.groupby('Region')['OrderID'].count().sort_values(ascending=False);

print(orders_by_region(myvar));

#Best performing Region
def best_perfoming_region(file):
    print('Best performing Region')
    return file.groupby('Region')['Revenue (Gross)'].sum().sort_values(ascending=True).head(1);

print(best_perfoming_region(myvar));

#Time Insights

# Monthly Sales Trend
def monthly_sales_trend(file):
    print('Monthly Sales Trend')
    file['OrderDate'] = pd.to_datetime(file['OrderDate'])
    return file.groupby(file['OrderDate'].dt.to_period('M'))['Revenue (Gross)'].sum().head();

print(monthly_sales_trend(myvar));

# Daily Orders Trend
def daily_orders_trend(file):
    print('Daily Orders Trend')
    file['OrderDate'] = pd.to_datetime(file['OrderDate'])
    return file.groupby(file['OrderDate'].dt.to_period('D'))['Revenue (Gross)'].sum().head();

print(daily_orders_trend(myvar));

# Highest sales month
def highest_sales_month(file):
    print('Highest sales month')
    file['OrderDate'] = pd.to_datetime(file['OrderDate'])
    return file.groupby(file['OrderDate'].dt.to_period('M'))['Revenue (Gross)'].sum().sort_values(ascending=False).head(1);

print(highest_sales_month(myvar));

# Pricing & Revenue Quality 

#Average Unit Price per Product
def avg_unit_price_per_product(file):
    print('Average Unit Price per Product')
    return file.groupby('Product')['UnitPrice'].mean();

print(avg_unit_price_per_product(myvar));

#Revenue per StoreLocation
def revenue_per_store_location(file):
    print('Revenue per StoreLocation')
    return file.groupby('StoreLocation')['Revenue (Gross)'].sum().sort_values(ascending=False);

print(revenue_per_store_location(myvar));

# Store Analysis

# Store-wise Revenue
def store_wise_revenue(file):
    print('Store-wise Revenue')
    return file.groupby('StoreLocation')['Revenue (Gross)'].sum().sort_values(ascending=False);

print(store_wise_revenue(myvar));

# Store-wise Orders
def store_wise_orders(file):
    print('Store-wise Orders');
    return file.groupby('StoreLocation')['OrderID'].count().sort_values(ascending=False);

print(store_wise_orders(myvar));

# Best performing Store
def best_performing_store(file):
    print('Best performing Store');
    return file.groupby('StoreLocation').agg({
        'OrderID': 'count',
        'Revenue (Gross)': 'sum'
    }).sort_values(by="Revenue (Gross)",ascending=False).head(1)

print(best_performing_store(myvar));

# Customer Insights

# Revenue by CustomerType (Retail vs Wholesale)
def revenue_by_customer_type(file):
    print('Revenue by CustomerType (Retail vs Wholesale)');
    return file.groupby('CustomerType')['Revenue (Gross)'].sum();

print(revenue_by_customer_type(myvar));

#Average order value per CustomerType
def avg_order_value_per_customer_type(file):
    print('Average order value per CustomerType');
    return file.groupby('CustomerType')['Revenue (Gross)'].mean();

print(avg_order_value_per_customer_type(myvar))

#Repeat customers (if possible)
def repeat_customers(file):
    print('Repeat customers (if possible)')
    return file.groupby('CustomerName')['OrderID'].count().sort_values(ascending=False).head();

print(repeat_customers(myvar));

# Payment Analysis

# Revenue by PaymentMethod
def revenue_by_payment_method(file):
    print('Revenue by PaymentMethod');
    return file.groupby('PaymentMethod')['Revenue (Gross)'].sum().sort_values(ascending=False).head();

print(revenue_by_payment_method(myvar))

#Most used payment method
def most_user_payment_method(file):
    print('Most used payment method');
    return file.groupby('PaymentMethod')['OrderID'].count().head();

print(most_user_payment_method(myvar))

# Promotion Analysis

# Revenue with vs without Promotion
def revenue_with_or_withot_promotion(file):
    print('Revenue with vs without Promotion');
    file['PromoStatus'] = file['Promotion'].apply(
        lambda x:'Without Promotion' if x == 'NOPROMOTION' else 'With Promotion'
    )
    return file.groupby('PromoStatus')['Revenue (Gross)'].sum().head();

print(revenue_with_or_withot_promotion(myvar))

#Best performing Promotion code
def best_performing_promotion_code(file):
    print('Best performing Promotion code');
    return file.groupby('Promotion')['Revenue (Gross)'].sum().head(1);

print(best_performing_promotion_code(myvar));

# Impact of Discount on sales
def impack_of_discount_on_sales(file):
    print('Impact of Discount on sales')

    file['IsDiscounted'] = file['Discount'].apply(
        lambda x:'' 'Not Discounted' if x == 0 else 'Discounted'
    )

    impact = file.groupby('IsDiscounted').agg({
        'Quantity':'sum',
        'Revenue (Gross)':'mean',
        'OrderID':'count'
    })

    # 3. Rename columns for a professional report
    impact.columns = ['Total Items Sold', 'Avg Revenue Per Sale', 'Transaction Count']

    return impact;

print(impack_of_discount_on_sales(myvar))







