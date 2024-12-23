from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Welcome to the AI Prediction API!"}

@app.route('/predict', methods=['POST'])
def predict():
    # Placeholder for future prediction functionality
    # Extend this endpoint to handle file uploads and make predictions
    return jsonify({"message": "Prediction endpoint coming soon!"})

if __name__ == '__main__':
    # Get the PORT environment variable provided by Render or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 so the app is externally accessible
    app.run(host='0.0.0.0', port=port, debug=True)
