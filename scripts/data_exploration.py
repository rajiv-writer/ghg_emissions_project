import pandas as pd

# Path to your Excel file
file_path = "../data/EDGAR_2024_GHG_booklet_2024.xlsx"

# Load all sheet names
sheet_names = pd.ExcelFile(file_path).sheet_names
print("Available Sheets:", sheet_names)

# Load and preview data from each sheet
for sheet in sheet_names:
    print(f"\nReading data from sheet: {sheet}")
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(df.head())
    print(df.info())
