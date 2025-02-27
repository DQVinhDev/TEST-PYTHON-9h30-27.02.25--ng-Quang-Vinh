from flask import Blueprint, request, jsonify
import pandas as pd
import os

sales_bp = Blueprint('sales', __name__)

# In-memory storage for the CSV data
sales_data = None

@sales_bp.route('/sales/', methods=['GET'])
def get_sales():
    global sales_data
    
    # check if there is any data available
    if sales_data is None:
        #check if the sales_data.csv file exists
        if not os.path.exists('../data/sales_data.csv'):
            return jsonify({"error": "No data available. Please upload a CSV file first."}), 400
        else:
            # If the file exists, read the data from the file
            sales_data = pd.read_csv('../data/sales_data.csv')
            sales_data['date'] = pd.to_datetime(sales_data['date'])
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    region = request.args.get('region')
    
    # Get query parameters for pagination
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    
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
    
    # Calculate start and end indices for pagination
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    
    # Get filtered data and apply pagination
    paginated_data = filtered_data.iloc[start_index:end_index]
    
    return jsonify({
        "total_sales": int(total_sales),
        "average_sales": float(average_sales),
        "transaction_count": transaction_count,
        "matching_records": paginated_data.to_dict('records'),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(filtered_data) + page_size - 1) // page_size
    }), 200 