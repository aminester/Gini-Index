import pandas as pd
import numpy as np
import warnings
import joblib

# For model building
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.sm_exceptions import ConvergenceWarning

# Suppress specific warnings for cleaner output
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# =====================
# Load and Prepare Data
# =====================

# Read the dataset
try:
    df = pd.read_csv('final_dataset.csv', delimiter=',', encoding='ISO-8859-1')
except FileNotFoundError:
    print("Error: 'final_dataset.csv' not found. Please ensure the file exists in the working directory.")
    exit(1)

# Rename columns if necessary
expected_columns = ['Country', 'Country Code', 'Year', 'Gini Coefficient']
if df.columns.tolist() != expected_columns:
    df.columns = expected_columns

# Convert 'Year' to numeric, coercing errors to NaN
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Convert 'Gini Coefficient' to numeric, coercing errors to NaN
df['Gini Coefficient'] = pd.to_numeric(df['Gini Coefficient'], errors='coerce')

# Drop rows with missing values in 'Country', 'Year', or 'Gini Coefficient'
df.dropna(subset=['Country', 'Year', 'Gini Coefficient'], inplace=True)

# Convert 'Year' to integer
df['Year'] = df['Year'].astype(int)

# Remove duplicate Year entries per Country
df = df.drop_duplicates(subset=['Country', 'Year'])

# Sort the data
df.sort_values(by=['Country', 'Year'], inplace=True)

# Reset index after sorting
df.reset_index(drop=True, inplace=True)

# =====================
# Model Building
# =====================

# Create a dictionary to store models for each country
models = {}

# Get the list of countries
countries = df['Country'].unique()

# Loop over each country and fit an ARIMA model
for country in countries:
    # Get the data for the country
    country_data = df[df['Country'] == country]

    # Check if there are enough data points
    if len(country_data) >= 5:  # Minimum of 5 data points required
        # Set the 'Year' as the index
        country_data = country_data.set_index('Year')

        # Convert the index to PeriodIndex with annual frequency
        try:
            country_data.index = pd.PeriodIndex(country_data.index, freq='Y-DEC')
        except Exception as e:
            print(f"Error setting PeriodIndex for {country}: {e}")
            continue

        # Get the Gini Coefficient series
        gini_series = country_data['Gini Coefficient']

        # Fit the ARIMA model with order (1,1,1)
        try:
            model = ARIMA(gini_series, order=(1, 1, 1))
            model_fit = model.fit()
            models[country] = model_fit
        except Exception as e:
            print(f"Could not fit ARIMA model for {country}: {e}")
    else:
        print(f"Not enough data to fit model for {country}")

# =====================
# Save the Models
# =====================

# Save the models dictionary to a file
joblib.dump(models, 'gini_models_arima.pkl')

print("Model training complete. ARIMA models saved to 'gini_models_arima.pkl'.")
