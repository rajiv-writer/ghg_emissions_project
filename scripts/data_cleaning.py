import os
import pandas as pd

# Ensure cleaned folder exists
cleaned_folder_path = "D:/ghg_emissions_project/data/cleaned/"
os.makedirs(cleaned_folder_path, exist_ok=True)

# Path to the original Excel file
file_path = "D:/ghg_emissions_project/data/EDGAR_2024_GHG_booklet_2024.xlsx"

# Load datasets
df_totals = pd.read_excel(file_path, sheet_name='GHG_totals_by_country')
df_sector = pd.read_excel(file_path, sheet_name='GHG_by_sector_and_country')
df_per_gdp = pd.read_excel(file_path, sheet_name='GHG_per_GDP_by_country')
df_per_capita = pd.read_excel(file_path, sheet_name='GHG_per_capita_by_country')

# Save cleaned datasets
df_totals.to_csv(cleaned_folder_path + "cleaned_ghg_totals.csv", index=False)
df_sector.to_csv(cleaned_folder_path + "cleaned_ghg_by_sector.csv", index=False)
df_per_gdp.to_csv(cleaned_folder_path + "cleaned_ghg_per_gdp.csv", index=False)
df_per_capita.to_csv(cleaned_folder_path + "cleaned_ghg_per_capita.csv", index=False)

print("✅ Data cleaning completed and files saved!")
