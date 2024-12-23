import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to validate and load data
def load_and_validate_excel(file_path):
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        return None, str(e)
    
    required_columns = ['Day', 'Price (VND)']
    if not all(col in data.columns for col in required_columns):
        return None, "Excel file must contain 'Day' and 'Price (VND)' columns."
    
    if data.isnull().values.any():
        return None, "The Excel file contains missing values. Please clean the data."
    
    return data, None

# Route: Home
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the AI Prediction API!"})

# Route: Upload and Predict
@app.route('/predict', methods=['POST'])
def predict():
    # Check if file is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400
    
    # Save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Load and validate the data
    data, error = load_and_validate_excel(file_path)
    if error:
        return jsonify({"error": error}), 400
    
    # Prepare data for training
    days = data['Day'].values.reshape(-1, 1)
    prices = data['Price (VND)'].values
    
    # Train the model
    model = LinearRegression()
    model.fit(days, prices)
    
    # Get user input for prediction days
    try:
        prediction_days = request.form.get('days')
        if not prediction_days:
            return jsonify({"error": "No prediction days provided."}), 400
        future_days = np.array([[int(day.strip())] for day in prediction_days.split(",")])
    except ValueError:
        return jsonify({"error": "Invalid days format. Provide comma-separated integers."}), 400
    
    # Predict prices
    predicted_prices = model.predict(future_days)
    predictions = {f"Day {day[0]}": f"{price:,.2f} VND" for day, price in zip(future_days, predicted_prices)}
    
    return jsonify({"predictions": predictions})

if __name__ == '__main__':
    app.run(debug=True)
