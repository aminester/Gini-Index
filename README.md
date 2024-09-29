# Gini Coefficient Predictor for 2030

<img width="1440" alt="Screenshot 2024-09-29 at 4 35 03 PM" src="https://github.com/user-attachments/assets/41593cc6-cbdb-48f5-8362-a2ccfb59f85e">


## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Data](#data)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
  - [Model Training](#model-training)
  - [Launching the Streamlit App](#launching-the-streamlit-app)
- [Project Structure](#project-structure)
- [Results](#results)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

The **Gini Coefficient Predictor for 2030** is a data-driven project designed to forecast the Gini Coefficient—a measure of income inequality—for various countries up to the year 2030. Utilizing time series analysis with ARIMA models, this project provides insightful predictions and visualizations through an interactive Streamlit web application.

## Features

- **Automated Model Training**: Fits ARIMA models for countries with sufficient historical Gini Coefficient data.
- **Interactive Web App**: Allows users to select a country and view predictions along with historical data.
- **Dynamic Visualizations**: Presents clear and informative plots showcasing historical trends and future forecasts.
- **Comprehensive Summaries**: Provides summaries of each country's Gini Coefficient trends over time.

## Data

- **Primary Dataset**: `final_dataset.csv`
  - **Columns**:
    - `Country`: Name of the country.
    - `Country Code`: ISO country code.
    - `Year`: Year of the recorded Gini Coefficient.
    - `Gini Coefficient`: Value representing income inequality.

- **Additional Dataset**: `country_blurbs.csv` *(Optional)*
  - **Columns**:
    - `Country`: Name of the country.
    - `Blurb`: Descriptive information about the country.

## Technologies Used

- **Programming Languages**: Python 3.12
- **Libraries & Frameworks**:
  - Data Manipulation: `pandas`, `numpy`
  - Statistical Modeling: `statsmodels`
  - Visualization: `matplotlib`, `seaborn`
  - Machine Learning: `joblib`
  - Web App: `Streamlit`
- **Environment Management**: `virtualenv` or `venv`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/gini-coefficient-predictor.git
   cd gini-coefficient-predictor
