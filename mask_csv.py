import os
import sys
# Import the Tonic Textual tool
from tonic_textual.api import TonicTextual

# 1. Get the API Key from GitHub Secrets
api_key = os.getenv('TONIC_TEXTUAL_API_KEY')
base_url = "https://textual.tonic.ai" 

if not api_key:
    print("Error: API Key is missing.")
    sys.exit(1)

client = TonicTextual(base_url, api_key)

# 2. Define your file names
input_file = "input.csv"    
output_file = "masked_output.csv"

print(f"Reading {input_file}...")

try:
    # 3. Read the CSV file
    with open(input_file, 'r', encoding='utf-8') as f:
        csv_content = f.read()

    # 4. Send to Tonic for Masking
    print("Sending CSV to Tonic.ai...")
    response = client.redact_csv(csv_content)

    # 5. Save the Clean CSV
    print(f"Masking complete. Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.redacted_text)

    print("Success!")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)