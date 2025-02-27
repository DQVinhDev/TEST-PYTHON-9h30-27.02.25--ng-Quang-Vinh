from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import io
import os

app = Flask(__name__)

# In-memory storage for the CSV data
sales_data = None

@app.route('/upload/', methods=['POST'])
def upload_csv():
    global sales_data
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be a CSV"}), 400
    
    try:
        # Read the file content
        file_content = file.read()
        
        # Convert to pandas DataFrame
        sales_data = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        
        # Convert date column to datetime
        sales_data['date'] = pd.to_datetime(sales_data['date'])
        
        # Calculate total price
        sales_data['total_price'] = sales_data['quantity'] * sales_data['price']
        
        return jsonify({
            "message": "File uploaded successfully",
            "rows": len(sales_data)
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sales/', methods=['GET'])
def get_sales():
    global sales_data
    
    if sales_data is None:
        return jsonify({"error": "No data available. Please upload a CSV file first."}), 400
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    region = request.args.get('region')
    
    # Create a copy of the data for filtering
    filtered_data = sales_data.copy()
    
    # Apply filters
    if start_date:
        try:
            start_date = pd.to_datetime(start_date)
            filtered_data = filtered_data[filtered_data['date'] >= start_date]
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD."}), 400
    
    if end_date:
        try:
            end_date = pd.to_datetime(end_date)
            filtered_data = filtered_data[filtered_data['date'] <= end_date]
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD."}), 400
    
    if region:
        filtered_data = filtered_data[filtered_data['region'] == region]
    
    # Calculate aggregations
    if len(filtered_data) == 0:
        return jsonify({
            "total_sales": 0,
            "average_sales": 0,
            "transaction_count": 0,
            "matching_records": []
        }), 200
    
    total_sales = filtered_data['total_price'].sum()
    average_sales = filtered_data['total_price'].mean()
    transaction_count = len(filtered_data)
    
    # Convert dates to string for JSON serialization
    filtered_data['date'] = filtered_data['date'].dt.strftime('%Y-%m-%d')
    
    return jsonify({
        "total_sales": total_sales,
        "average_sales": average_sales,
        "transaction_count": transaction_count,
        "matching_records": filtered_data.to_dict('records')
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)