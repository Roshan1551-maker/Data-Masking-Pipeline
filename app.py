from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from faker import Faker
import os

app = Flask(__name__)

# Set path for both input and output files
base_path = r'D:\Fiver\Ietazaz\Huraira'
app.config['UPLOAD_FOLDER'] = base_path
app.config['MASKED_FOLDER'] = base_path

faker = Faker()  # Initialize Faker instance for generating fake data
consistent_data = {}  # Dictionary to store consistent data for certain fields

# Function to retrieve or create consistent data for specified fields
def get_consistent_data(key, faker_function):
    if key not in consistent_data:
        consistent_data[key] = faker_function()  # Store consistent data for reuse
    return consistent_data[key]

# Function to apply masking rules to the data in the CSV file
def mask_data(input_csv, output_csv):
    df = pd.read_csv(input_csv)  # Read data from the input CSV file

    def mask_row(row):
        # Mask name field consistently for specific keys
        row['name'] = get_consistent_data(row['name'], faker.name)
        
        # Mask phone number field with random fake phone number
        row['phone_number'] = faker.phone_number()
        
        # Mask email field with consistent fake emails based on name
        row['email'] = get_consistent_data(row['name'], faker.email)
        
        return row

    # Apply the mask_row function to each row in the DataFrame
    masked_df = df.apply(mask_row, axis=1)
    
    # Save the masked data to the output CSV file
    masked_df.to_csv(output_csv, index=False)

@app.route('/')
def index():
    # Render the main interface HTML page
    return render_template('index.html')

@app.route('/mask', methods=['POST'])
def mask():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], "input_data.csv")  # Input file path
        file.save(input_path)
        
        output_filename = "masked_input_data.csv"  # Output file name
        output_path = os.path.join(app.config['MASKED_FOLDER'], output_filename)  # Output file path
        
        # Apply the data masking function
        mask_data(input_path, output_path)
        
        return render_template('index.html', masked_file=f"/masked_files/{output_filename}")
    return "Invalid file format. Please upload a CSV file."

@app.route('/masked_files/<filename>')
def download_file(filename):
    # Send the masked file for download to the user
    return send_from_directory(app.config['MASKED_FOLDER'], filename)

if __name__ == '__main__':
    # Start the Flask web server
    app.run(debug=True)
