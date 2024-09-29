import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# =====================
# Load Data and Models
# =====================

# Load the primary dataset
try:
    df = pd.read_csv('final_dataset.csv', delimiter=',', encoding='ISO-8859-1')
except FileNotFoundError:
    st.error("Error: 'final_dataset.csv' not found. Please ensure the file exists in the working directory.")
    st.stop()

# Rename columns if necessary
expected_columns = ['Country', 'Country Code', 'Year', 'Gini Coefficient']
if df.columns.tolist() != expected_columns:
    df.columns = expected_columns

# Convert 'Year' and 'Gini Coefficient' to numeric
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Gini Coefficient'] = pd.to_numeric(df['Gini Coefficient'], errors='coerce')

# Drop rows with missing values
df.dropna(subset=['Country', 'Year', 'Gini Coefficient'], inplace=True)

# Convert 'Year' to integer
df['Year'] = df['Year'].astype(int)

# Load the trained models
try:
    models = joblib.load('gini_models_arima.pkl')
except FileNotFoundError:
    st.error("Model file 'gini_models_arima.pkl' not found. Please run 'model.py' first.")
    st.stop()

# =====================
# Streamlit App
# =====================

# Set page configuration
st.set_page_config(
    page_title="Gini Coefficient Predictor for 2030",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Set page title with styling
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Gini Coefficient Predictor for 2030</h1>", unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header('📊 Select a Country')

# Get a list of countries with models
countries_with_models = list(models.keys())
selected_country = st.sidebar.selectbox('Country', sorted(countries_with_models))

# Get data for the selected country
country_data = df[df['Country'] == selected_country].copy()

# Prepare data for prediction
if selected_country in models:
    model = models[selected_country]

    # Forecasting to 2030
    last_year = int(country_data['Year'].max())
    target_year = 2030
    years_ahead = target_year - last_year
    if years_ahead <= 0:
        st.warning(f"{selected_country} already has data up to or beyond {target_year}.")
    else:
        try:
            # Generate forecast
            forecast = model.predict(start=last_year + 1, end=target_year)
            predicted_gini_2030 = forecast.iloc[-1]

            # Display the prediction with styling
            st.markdown(f"### 📈 Predicted Gini Coefficient for {selected_country} in {target_year}")
            st.write(f"**{predicted_gini_2030:.4f}**")

            # Plot historical and forecasted Gini Coefficient
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=country_data, x='Year', y='Gini Coefficient', marker='o', label='Historical', color='#1F618D')

            # Create a DataFrame for forecast
            forecast_years = list(range(last_year + 1, target_year + 1))
            forecast_values = forecast.values
            forecast_df = pd.DataFrame({
                'Year': forecast_years,
                'Gini Coefficient': forecast_values
            })

            sns.lineplot(data=forecast_df, x='Year', y='Gini Coefficient', marker='o', linestyle='--', color='#E67E22', label='Forecasted')

            plt.title(f'Gini Coefficient Trend for {selected_country}', fontsize=16)
            plt.xlabel('Year', fontsize=14)
            plt.ylabel('Gini Coefficient', fontsize=14)
            plt.legend(fontsize=12)
            plt.grid(True)
            plt.tight_layout()
            st.pyplot(plt)

            # Display Country Statistics Summary
            earliest_year = country_data['Year'].min()
            latest_year = country_data['Year'].max()
            earliest_gini = country_data[country_data['Year'] == earliest_year]['Gini Coefficient'].values[0]
            latest_gini = country_data[country_data['Year'] == latest_year]['Gini Coefficient'].values[0]

            # Determine trend
            if latest_gini > earliest_gini:
                trend = "increased"
            elif latest_gini < earliest_gini:
                trend = "decreased"
            else:
                trend = "remained stable"

            # Create summary sentences
            summary = f"From **{earliest_year}** to **{latest_year}**, {selected_country}'s Gini Coefficient **{trend}** from **{earliest_gini:.4f}** to **{latest_gini:.4f}**."

            st.markdown("### 📑 Country Statistics Summary")
            st.write(summary)

        except Exception as e:
            st.error(f"Error during forecasting: {e}")
else:
    st.warning(f"No model available for {selected_country}.")
