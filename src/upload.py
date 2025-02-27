from flask import Blueprint, request, jsonify
import pandas as pd
import io
import os

upload_bp = Blueprint('upload', __name__)

# In-memory storage for the CSV data
sales_data = None

@upload_bp.route('/upload/', methods=['POST'])
def upload_csv():
    global sales_data
    
    # Print the information of the uploaded file
    print(request.files)
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Check the file format
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be a CSV"}), 400
    
    try:
        # Read the file content
        file_content = file.read()
        
        # Convert the content to a pandas DataFrame
        sales_data = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        
        # Convert the date column to datetime format
        sales_data['date'] = pd.to_datetime(sales_data['date'])
        
        # Calculate total price
        sales_data['total_price'] = sales_data['quantity'] * sales_data['price']
        
        # Save the DataFrame to a CSV file
        sales_data.to_csv('../data/sales_data.csv', index=False)
        
        return jsonify({
            "message": "File uploaded successfully",
            "rows": len(sales_data)
        }), 200
    
    except Exception as e:
        # Print the error if any
        print("Error uploading file:", str(e))
        return jsonify({"error": str(e)}), 500 