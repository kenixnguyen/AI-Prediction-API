from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Welcome to the AI Prediction API!"}

@app.route('/predict', methods=['POST'])
def predict():
    # Example endpoint for future expansion
    return jsonify({"message": "Prediction endpoint coming soon!"})

if __name__ == '__main__':
    app.run(debug=True)
