# mask_csv.py
import os
import sys
from io import StringIO

# Use the modern SDK entry points:
from tonic_textual.redact_api import TextualNer
from tonic_textual.helpers.csv_helper import CsvHelper

# 1) Get the API Key from environment (GitHub secret)
api_key = os.getenv("TONIC_TEXTUAL_API_KEY")
if not api_key:
    print("Error: TONIC_TEXTUAL_API_KEY environment variable is missing.")
    sys.exit(1)

# 2) Initialize clients
try:
    ner = TextualNer(api_key=api_key)
    helper = CsvHelper()
except Exception as e:
    print(f"Error initializing Tonic SDK: {e}")
    sys.exit(1)

# 3) Filenames (must match files in the repo)
INPUT_FILE = "input.csv"
OUTPUT_FILE = "masked_output.csv"

def redact_text_fn(text):
    """
    Helper wrapper around ner.redact(...) to return a plain string.
    The SDK may return objects; handle common shapes safely.
    """
    try:
        resp = ner.redact(text)
        # Try common attributes in order
        if resp is None:
            return ""
        if isinstance(resp, str):
            return resp
        # some SDK responses expose 'redacted_text' or 'text'
        for attr in ("redacted_text", "redacted", "text"):
            if hasattr(resp, attr):
                val = getattr(resp, attr)
                if callable(val):
                    # guard: if attribute is callable, call it
                    return val()
                return val
        # fallback to string conversion
        return str(resp)
    except Exception as e:
        # Do not crash whole job for a single text — but surface the error
        print(f"Warning: redact() failed for a value. Error: {e}")
        # returning original text as a safe fallback (adjust if you want failure instead)
        return text

def main():
    if not os.path.isfile(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found in repository root.")
        sys.exit(1)

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as fh:
            # Use CsvHelper to redact and reconstruct CSV
            # Note: change conversation_id_column and message_column to match your CSV header names
            buf = helper.redact_and_reconstruct(
                fh,
                has_header=True,
                conversation_id_column="conversation_id",
                message_column="message",
                redact_function=lambda t: redact_text_fn(t),
            )

        # buf is a file-like object (StringIO). Write to output file.
        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as out_f:
            out_f.write(buf.getvalue())

        print(f"Success: wrote masked output to '{OUTPUT_FILE}'.")

    except Exception as exc:
        print("Error during masking process:", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
