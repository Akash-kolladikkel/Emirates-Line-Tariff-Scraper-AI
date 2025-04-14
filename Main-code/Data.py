import os
import pandas as pd
import re
from pathlib import Path
import io
from docling.document_converter import DocumentConverter
import google.generativeai as genai
from dotenv import load_dotenv

# Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# Setup paths
excel_folder = Path("Excel-Files")
csv_folder = Path("CSV-Files")

# Get files
excel_files = list(excel_folder.glob("*.xlsx"))
print(f"Found {len(excel_files)} Excel files")

processed = 0
errors = []

for file_path in excel_files:
    try:
        # Extract country-port from filename
        filename = file_path.stem
        country, port = re.split(r"[-_]", filename, 1)
        port = port.replace("-", " ").replace("_", " ").title()

        # Convert Excel to Markdown
        converter = DocumentConverter()
        result = converter.convert(file_path)
        md_data = result.document.export_to_markdown()

        # Generate AI prompt
        prompt =  f"""
Analyze this shipping data and extract the following structured information:

Required Fields:
- S.N (Sequential Number)
- Country: {country}
- Line (ESL)
- Port: {port}
- Equipment Type (e.g: Dry, Reefer, Tank)
- Currency
- Free Days
- Bucket 1 
- Bucket 2 
- Bucket 3 
- Local Charges (if available)

Bucket Rules:
1. Free Days = 0-5 days (no charges)
2. Bucket 1 = 6-10 days
3. Bucket 2 = 11-15 days
4. Bucket 3 = 16-9999 days
Note: Different equipment types may have different free days and bucket ranges - preserve these variations.

Input Data:
{{data}}  # Double curly braces for proper formatting

Return Format (JSON):
{{
  "data": [
    {{
      "S.N": int,
      "Country": "{country}",
      "Line": str,
      "Port": "{port}",
      "Equipment_Type": str, #Format: "20-Dry"
      "Currency": str,
      "Free_days": int,
      "Bucket 1 (6-10)": str, 
      "Bucket 2 (11-15)": str,
      "Bucket 3 (16-9999)": str,
      "Local_Charges": str | null
    }}
  ]
}}

Input data:
{md_data}
"""

        # Get AI response
        response = model.generate_content(prompt)
        json_str = response.text[response.text.find('{'):response.text.rfind('}')+1]

        # Save CSV
        df = pd.read_json(io.StringIO(json_str))   
        df = pd.json_normalize(df['data'])
        output_path = csv_folder / f"{country}-{port}.csv"
        df.to_csv(output_path, index=False)
        
        print(f"Processed: {filename}")
        processed += 1

    except Exception as e:
        errors.append(f"{filename}: {str(e)}")
        print(f"Failed {filename}")

# Final report
print(f"\nSuccess: {processed}/{len(excel_files)}")
if errors:
    print("\nErrors:")
    for error in errors:
        print(f"- {error}")