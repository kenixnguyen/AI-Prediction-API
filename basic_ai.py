import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Sample data for demonstration
data = pd.DataFrame({
    'Day': [1, 2, 3, 4, 5],
    'Price (VND)': [100000, 110000, 120000, 130000, 140000]
})

# Convert data into numpy arrays
days = data['Day'].values.reshape(-1, 1)  # Independent variable
prices = data['Price (VND)'].values       # Dependent variable

# Create and train a Linear Regression model
model = LinearRegression()
model.fit(days, prices)

# Predict prices for future days
future_days = np.array([[6], [7], [8]])
predicted_prices = model.predict(future_days)

# Print predictions
print("Predictions:")
for day, price in zip(future_days.flatten(), predicted_prices):
    print(f"Day {day}: {price:,.2f} VND")

# Plot the results
plt.scatter(days, prices, color='blue', label='Actual Data')
plt.plot(days, model.predict(days), color='red', label='Regression Line')
plt.scatter(future_days, predicted_prices, color='green', label='Predicted Prices')
plt.title('Price Prediction')
plt.xlabel('Day')
plt.ylabel('Price (VND)')
plt.legend()
plt.show()
