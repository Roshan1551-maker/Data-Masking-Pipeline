from app import mask_data
import os

input_file = 'input_data.csv'
output_file = 'masked_output.csv'

# Check if the file is there
if os.path.exists(input_file):
    print("Found the file! Masking it now...")
    #  Runs original masking logic
    mask_data(input_file, output_file)
    print("Done! Data is masked.")
else:
    print("Error: Could not find input_data.csv")