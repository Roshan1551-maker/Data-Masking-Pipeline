import os
import sys
# CORRECT IMPORT: The class is in 'redact_api', not 'api'
from tonic_textual.redact_api import TextualNer

# 1. Get the API Key
api_key = os.getenv('TONIC_TEXTUAL_API_KEY')
if not api_key:
    print("Error: TONIC_TEXTUAL_API_KEY is missing.")
    sys.exit(1)

# 2. Initialize the client (Use TextualNer for the latest version)
try:
    client = TextualNer(api_key=api_key)
except Exception as e:
    print(f"Error initializing client: {e}")
    sys.exit(1)

# 3. File Names
input_file = "input.csv"    
output_file = "masked_output.csv"

print(f"Reading {input_file}...")

try:
    # 4. Read the CSV file as text
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        sys.exit(1)
        
    with open(input_file, 'r', encoding='utf-8') as f:
        csv_content = f.read()

    # 5. Send to Tonic for Masking
    print("Sending content to Tonic.ai...")
    # 'redact' is the universal method that works on any text/csv string
    response = client.redact(csv_content)

    # 6. Save the Clean CSV
    print(f"Masking complete. Saving to {output_file}...")
    
    # Securely handle the response object
    final_text = response.redacted_text
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_text)

    print("Success: masked_output.csv created.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    sys.exit(1)

