# Import necessary libraries
import pandas as pd
import numpy as np
import country_converter as coco

# Define a function to clean the 'Country' column
def clean_country_column(df, country_column):
    # Remove rows where country is missing or not a string
    df = df[df[country_column].notnull()]
    df = df[df[country_column].apply(lambda x: isinstance(x, str))]
    # Strip whitespace
    df[country_column] = df[country_column].str.strip()
    # Get a list of valid country names
    cc = coco.CountryConverter()
    valid_countries = set(cc.data['name_short'])
    # Remove rows where country is not in valid_countries
    df = df[df[country_column].isin(valid_countries)]
    return df

# Define a function to standardize country names
def standardize_country_names(df, country_column):
    # Convert country names to standardized short names
    df[country_column] = coco.convert(names=df[country_column], to='name_short', not_found=None)
    # Remove rows where country conversion failed
    df = df[df[country_column].notnull()]
    return df

# =====================
# Read and Process Gini Coefficient Data
# =====================

# Read Gini Coefficient Data
gini_df = pd.read_csv(
    'Data/Gini Index/economic-inequality-gini-index.csv',
    encoding='ISO-8859-1')

# Rename columns for consistency
gini_df.columns = ['Country', 'Country Code', 'Year', 'Gini Coefficient']

# Ensure 'Year' is numeric
gini_df['Year'] = pd.to_numeric(gini_df['Year'], errors='coerce')

# Ensure 'Gini Coefficient' is numeric
gini_df['Gini Coefficient'] = pd.to_numeric(gini_df['Gini Coefficient'], errors='coerce')

# Clean 'Country' column
gini_df = clean_country_column(gini_df, 'Country')

# Standardize country names
gini_df = standardize_country_names(gini_df, 'Country')

# =====================
# Read and Process GDP per Capita Data
# =====================

# Read GDP per Capita Data
gdp_per_capita_df = pd.read_csv(
    'Data/GDP per Capita/SYB66_230_202310_GDP and GDP Per Capita.csv',
    encoding='ISO-8859-1', skiprows=2)

# Correct column names
gdp_per_capita_df.columns = ['Code', 'Country', 'Year', 'Series', 'Value', 'Footnotes', 'Source']

# Keep necessary columns
gdp_per_capita_df = gdp_per_capita_df[['Country', 'Year', 'Series', 'Value']]

# Clean 'Country' column
gdp_per_capita_df = clean_country_column(gdp_per_capita_df, 'Country')

# Standardize country names
gdp_per_capita_df = standardize_country_names(gdp_per_capita_df, 'Country')

# Clean 'Value' column
gdp_per_capita_df['Value'] = gdp_per_capita_df['Value'].replace(',', '', regex=True)
gdp_per_capita_df['Value'] = pd.to_numeric(gdp_per_capita_df['Value'], errors='coerce')

# Ensure 'Series' column contains only strings
gdp_per_capita_df['Series'] = gdp_per_capita_df['Series'].astype(str)

# Pivot 'Series' to columns
gdp_per_capita_df = gdp_per_capita_df.pivot_table(
    index=['Country', 'Year'], columns='Series', values='Value', aggfunc='mean').reset_index()

# =====================
# Read and Process Health Expenditure Data
# =====================

# Read Health Expenditure Data
health_expenditure_df = pd.read_csv(
    'Data/Expenditure on Health/SYB66_325_202310_Expenditure on health.csv',
    encoding='ISO-8859-1', skiprows=2)

# Correct column names
health_expenditure_df.columns = ['Code', 'Country', 'Year', 'Series', 'Value', 'Footnotes', 'Source']

# Keep necessary columns
health_expenditure_df = health_expenditure_df[['Country', 'Year', 'Series', 'Value']]

# Clean 'Country' column
health_expenditure_df = clean_country_column(health_expenditure_df, 'Country')

# Standardize country names
health_expenditure_df = standardize_country_names(health_expenditure_df, 'Country')

# Convert 'Value' to numeric
health_expenditure_df['Value'] = pd.to_numeric(health_expenditure_df['Value'], errors='coerce')

# Ensure 'Series' column contains only strings
health_expenditure_df['Series'] = health_expenditure_df['Series'].astype(str)

# Pivot 'Series' to columns
health_expenditure_df = health_expenditure_df.pivot_table(
    index=['Country', 'Year'], columns='Series', values='Value', aggfunc='mean').reset_index()

# =====================
# Read and Process Enrollment Data
# =====================

# Read Enrollment Data
enrollment_df = pd.read_csv(
    'Data/Enrollment in primary, lower secondary and upper secondary education levels/SYB66_309_202310_Education.csv',
    encoding='ISO-8859-1', skiprows=2)

# Correct column names
enrollment_df.columns = ['Code', 'Country', 'Year', 'Series', 'Value', 'Footnotes', 'Source']

# Keep necessary columns
enrollment_df = enrollment_df[['Country', 'Year', 'Series', 'Value']]

# Clean 'Country' column
enrollment_df = clean_country_column(enrollment_df, 'Country')

# Standardize country names
enrollment_df = standardize_country_names(enrollment_df, 'Country')

# Clean 'Value' column
enrollment_df['Value'] = enrollment_df['Value'].replace(',', '', regex=True)
enrollment_df['Value'] = pd.to_numeric(enrollment_df['Value'], errors='coerce')

# Ensure 'Series' column contains only strings
enrollment_df['Series'] = enrollment_df['Series'].astype(str)

# Pivot 'Series' to columns
enrollment_df = enrollment_df.pivot_table(
    index=['Country', 'Year'], columns='Series', values='Value', aggfunc='mean').reset_index()

# =====================
# Read and Process Labor Force and Unemployment Data
# =====================

# Read Labor Force and Unemployment Data
labor_unemployment_df = pd.read_csv(
    'Data/Labor Force and Unemployment/SYB66_329_202310_Labour Force and Unemployment.csv',
    encoding='ISO-8859-1', skiprows=2)

# Correct column names
labor_unemployment_df.columns = ['Code', 'Country', 'Year', 'Series', 'Value', 'Footnotes', 'Source']

# Keep necessary columns
labor_unemployment_df = labor_unemployment_df[['Country', 'Year', 'Series', 'Value']]

# Clean 'Country' column
labor_unemployment_df = clean_country_column(labor_unemployment_df, 'Country')

# Standardize country names
labor_unemployment_df = standardize_country_names(labor_unemployment_df, 'Country')

# Convert 'Value' to numeric
labor_unemployment_df['Value'] = pd.to_numeric(labor_unemployment_df['Value'], errors='coerce')

# Ensure 'Series' column contains only strings
labor_unemployment_df['Series'] = labor_unemployment_df['Series'].astype(str)

# Pivot 'Series' to columns
labor_unemployment_df = labor_unemployment_df.pivot_table(
    index=['Country', 'Year'], columns='Series', values='Value', aggfunc='mean').reset_index()

# =====================
# Merge DataFrames
# =====================

# Merge Gini Data with GDP per Capita Data
merged_df = pd.merge(gini_df, gdp_per_capita_df, on=['Country', 'Year'], how='left')

# Merge with Health Expenditure Data
merged_df = pd.merge(merged_df, health_expenditure_df, on=['Country', 'Year'], how='left')

# Merge with Enrollment Data
merged_df = pd.merge(merged_df, enrollment_df, on=['Country', 'Year'], how='left')

# Merge with Labor Force and Unemployment Data
merged_df = pd.merge(merged_df, labor_unemployment_df, on=['Country', 'Year'], how='left')

# =====================
# Final Data Cleaning
# =====================

# Drop rows where 'Gini Coefficient' is missing
merged_df = merged_df.dropna(subset=['Gini Coefficient'])

# Optionally, drop columns with more than 50% missing values
threshold = len(merged_df) * 0.5
merged_df = merged_df.loc[:, merged_df.isnull().sum() < threshold]

# Fill remaining missing values with mean for numeric columns
numeric_cols = merged_df.select_dtypes(include=['float64', 'int64']).columns
merged_df[numeric_cols] = merged_df[numeric_cols].fillna(merged_df[numeric_cols].mean())

# Remove duplicates
merged_df = merged_df.drop_duplicates()

# Reset index
merged_df.reset_index(drop=True, inplace=True)

# =====================
# Save Final Dataset
# =====================

# Save the final merged dataset to a CSV file
merged_df.to_csv('final_dataset.csv', index=False)

print("Data processing complete. The final dataset has been saved to 'final_dataset.csv'.")
