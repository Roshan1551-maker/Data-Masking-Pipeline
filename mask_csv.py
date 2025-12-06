import os
import sys
from tonic_textual.api import TonicTextual

# 1. Get the API Key from GitHub Secrets
api_key = os.getenv('TONIC_TEXTUAL_API_KEY')
base_url = "https://textual.tonic.ai" 

if not api_key:
    print("Error: TONIC_TEXTUAL_API_KEY is missing.")
    sys.exit(1)

# 2. Initialize the main Client (This handles everything)
client = TonicTextual(base_url, api_key)

# 3. Define File Names
input_file = "input.csv"    
output_file = "masked_output.csv"

print(f"Reading {input_file}...")

try:
    # 4. Read the CSV file
    with open(input_file, 'r', encoding='utf-8') as f:
        csv_content = f.read()

    # 5. Send to Tonic for Masking
    # usage of the simple API designed for CSVs
    print("Sending CSV to Tonic.ai...")
    response = client.redact_csv(csv_content)

    # 6. Save the Clean CSV
    print(f"Masking complete. Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(response.redacted_text)

    print("Success: Wrote masked output.")

except Exception as e:
    print(f"Error during masking: {e}")
    sys.exit(1)
