import os
import sys
from tonic_textual.redact_api import TextualNer
from tonic_textual.helpers.csv_helper import CsvHelper

# Get the API Key
api_key = os.getenv('TONIC_TEXTUAL_API_KEY')
if not api_key:
    print("Error: API Key is missing.")
    sys.exit(1)

# Initialize Tonic SDK
ner = TextualNer(api_key=api_key)
helper = CsvHelper()

# File names
input_file = "input.csv"
output_file = "masked_output.csv"

print(f"Reading {input_file}...")

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        # Redact CSV using conversation_id and message fields
        buf = helper.redact_and_reconstruct(
            f, has_header=True,
            conversation_id_column='conversation_id',
            message_column='message',
            redact_function=lambda x: ner.redact(x)
        )

    print(f"Writing masked data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(buf.getvalue())

    print("Success!")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
