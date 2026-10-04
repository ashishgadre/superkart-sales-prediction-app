# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
supercart_sales_predictor_api = Flask("SuperKart Sales Prediction Platform")

# Load the trained machine learning model
model = joblib.load("superkart_sales_model.joblib")

# Define a route for the home page (GET request)
@supercart_sales_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction Platform API!"

# Define an endpoint for single property prediction (POST request)
@supercart_sales_predictor_api.post('/v1/predict')
def predict_sales():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product details and returns
    the predicted sales price as a JSON response.
    """
    # Get the JSON data from the request body
    data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category'],
        'Product_Id_char': data['Product_Id_char']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_sales = model.predict(input_data).toList()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': predicted_sales})

# Define an endpoint to predict sales for a batch of products
@supercart_sales_predictor_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Create an output dictionary mapping row index to predicted sales
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}

    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    supercart_sales_predictor_api.run(debug=True)
