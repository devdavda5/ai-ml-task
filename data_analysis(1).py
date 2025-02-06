import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
transaction_file_path = "C:/Users/devda/Downloads/transaction_data.xlsx"
purchase_file_path = "C:/Users/devda/Downloads/purchase_behaviour.csv"

# Read the Excel file (assuming first sheet)
transaction_data = pd.read_excel(transaction_file_path)

# Read the CSV file
purchase_data = pd.read_csv(purchase_file_path)

# Convert DATE from serial format to datetime
transaction_data["DATE"] = pd.to_datetime(transaction_data["DATE"], origin="1899-12-30", unit="D")

# Merge datasets on LYLTY_CARD_NBR to include customer segmentation data
merged_data = transaction_data.merge(purchase_data, on="LYLTY_CARD_NBR", how="left")

# Total spending by LIFESTAGE and PREMIUM_CUSTOMER
spending_by_segment = merged_data.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"])["TOT_SALES"].sum().reset_index()

# Identify top 3 most profitable products
top_profitable_products = merged_data.groupby("PROD_NAME")["TOT_SALES"].sum().reset_index().sort_values(by="TOT_SALES", ascending=False).head(3)

# Identifying most loyal customers (highest number of transactions)
loyal_customers = merged_data.groupby("LYLTY_CARD_NBR").agg({"TXN_ID": "count", "TOT_SALES": "sum"}).reset_index()
loyal_customers.rename(columns={"TXN_ID": "NUM_TRANSACTIONS"}, inplace=True)
most_loyal_customers = loyal_customers.sort_values(by=["NUM_TRANSACTIONS", "TOT_SALES"], ascending=[False, False]).head(10)

# Analyzing characteristics of most loyal customers
loyal_customer_segments = merged_data[merged_data["LYLTY_CARD_NBR"].isin(most_loyal_customers["LYLTY_CARD_NBR"])].groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"]).size().reset_index(name="COUNT")

# Visualization
plt.figure(figsize=(12, 6))
sns.barplot(data=spending_by_segment, x="LIFESTAGE", y="TOT_SALES", hue="PREMIUM_CUSTOMER")
plt.title("Total Spending by Customer Segment")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(data=top_profitable_products, x="PROD_NAME", y="TOT_SALES")
plt.title("Top 3 Most Profitable Products")
plt.xticks(rotation=45, ha='right')
plt.show()

plt.figure(figsize=(12, 6))
sns.barplot(data=loyal_customer_segments, x="LIFESTAGE", y="COUNT", hue="PREMIUM_CUSTOMER")
plt.title("Characteristics of Most Loyal Customers")
plt.xticks(rotation=45)
plt.show()

# Summary Insights
print("Top Spending Customer Segments:\n", spending_by_segment.sort_values(by="TOT_SALES", ascending=False).head(5))
print("\nTop 3 Most Profitable Products:\n", top_profitable_products)
print("\nMost Loyal Customers:\n", most_loyal_customers)
print("\nCharacteristics of Most Loyal Customers:\n", loyal_customer_segments)