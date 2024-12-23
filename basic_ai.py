import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime

# Function to load the latest Excel file from the current directory
def load_latest_excel():
    excel_files = [file for file in os.listdir() if file.endswith('.xlsx')]
    if not excel_files:
        raise FileNotFoundError("No Excel files found in the current directory!")
    latest_file = max(excel_files, key=os.path.getmtime)
    print(f"Loaded file: {latest_file}")
    return pd.read_excel(latest_file)

# Function to save predictions to a new Excel file
def save_predictions_to_excel(future_days, predicted_prices):
    output_data = pd.DataFrame({
        'Day': future_days.flatten(),
        'Predicted Price (VND)': [f"{price:,.2f}" for price in predicted_prices]
    })
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"predictions_{timestamp}.xlsx"
    output_data.to_excel(output_filename, index=False)
    print(f"Predictions saved to: {output_filename}")

# Function to log predictions to a CSV file
def log_predictions(future_days, predicted_prices):
    log_data = pd.DataFrame({
        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(future_days),
        'Day': future_days.flatten(),
        'Predicted Price (VND)': [f"{price:,.2f}" for price in predicted_prices]
    })
    log_filename = "predictions_log.csv"
    if os.path.exists(log_filename):
        log_data.to_csv(log_filename, mode='a', header=False, index=False)
    else:
        log_data.to_csv(log_filename, index=False)
    print(f"Predictions logged to: {log_filename}")

# Load data
try:
    data = load_latest_excel()
except FileNotFoundError as e:
    print(e)
    exit()

# Validate data
required_columns = ['Day', 'Price (VND)']
if not all(col in data.columns for col in required_columns):
    print("Error: Missing required columns in the Excel file. Ensure the file has 'Day' and 'Price (VND)' columns.")
    exit()

if data.isnull().values.any():
    print("Error: The Excel file contains missing values. Please clean the data and try again.")
    exit()

# Convert data to arrays
days = data['Day'].values.reshape(-1, 1)
prices = data['Price (VND)'].values

# Create a linear regression model
model = LinearRegression()
model.fit(days, prices)

# Print model information
print("Regression coefficient (Slope):", model.coef_[0])
print("Intercept:", model.intercept_)

# Get user input for predictions
try:
    user_input = input("Enter the days for prediction (comma-separated, e.g., 6,7,8): ")
    future_days = np.array([[int(day.strip())] for day in user_input.split(",")])
except ValueError:
    print("Invalid input. Please enter a list of numbers separated by commas.")
    exit()

# Predict prices for user-defined days
predicted_prices = model.predict(future_days)

# Print predictions
print("\nPredicted prices for user-defined days:")
for day, price in zip(future_days.flatten(), predicted_prices):
    print(f"Day {day}: {price:,.2f} VND")

# Save predictions to Excel
save_predictions_to_excel(future_days, predicted_prices)

# Log predictions to CSV
log_predictions(future_days, predicted_prices)

# Plot the data and regression line
plt.scatter(days, prices, color='blue', label='Actual Data')
plt.plot(days, model.predict(days), color='red', label='Regression Line')

# Plot future predictions
plt.scatter(future_days, predicted_prices, color='green', label='User Predictions')

# Configure the plot
plt.title('Product Price Prediction')
plt.xlabel('Day')
plt.ylabel('Price (VND)')
plt.legend()
plt.show()
