import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# Load and Prepare Data
# =====================

# Attempt to read the CSV file with appropriate parameters
df = pd.read_csv('final_dataset.csv', delimiter=',', encoding='ISO-8859-1')  # Adjust as needed

# Print the columns to verify
print("Columns before renaming:", df.columns.tolist())

# If the columns are incorrect, rename them
if df.columns.tolist() == ['T', 'T.1', 'T.2', 'T.3']:
    df.columns = ['Country', 'Country Code', 'Year', 'Gini Coefficient']

# Verify the columns
print("Columns after renaming:", df.columns.tolist())

# Convert 'Year' and 'Gini Coefficient' to numeric
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Gini Coefficient'] = pd.to_numeric(df['Gini Coefficient'], errors='coerce')

# Drop rows with missing values in key columns
df.dropna(subset=['Country', 'Year', 'Gini Coefficient'], inplace=True)

# Display the first few rows
print(df.head())

# =====================
# Exploratory Data Analysis
# =====================

# Analyze the distribution of Gini Coefficient
plt.figure(figsize=(10, 6))
sns.histplot(df['Gini Coefficient'], bins=30, kde=True)
plt.title('Distribution of Gini Coefficient')
plt.xlabel('Gini Coefficient')
plt.ylabel('Frequency')
plt.show()

# Time Series Analysis
gini_yearly = df.groupby('Year')['Gini Coefficient'].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=gini_yearly, x='Year', y='Gini Coefficient')
plt.title('Average Gini Coefficient Over Time')
plt.xlabel('Year')
plt.ylabel('Average Gini Coefficient')
plt.show()
