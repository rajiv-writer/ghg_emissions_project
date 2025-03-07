import os
import pandas as pd
import psycopg2

DB_NAME = "ghg_emissions"
DB_USER = "postgres"
DB_PASS = "pwd333"
DB_HOST = "localhost"
DB_PORT = "5432"

cleaned_data_path = "D:/ghg_emissions_project/data/cleaned/"

def insert_data_to_db(filename, table_name, id_vars, value_name):
    file_path = os.path.join(cleaned_data_path, filename)

    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} NOT FOUND.")
        return

    df = pd.read_csv(file_path)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Ensure necessary columns exist
    if not set(id_vars).issubset(df.columns):
        print(f"❌ Error: Missing required columns in {filename}")
        print(f"Available columns: {df.columns}")
        return

    print(f"📊 Processing {filename} - Columns: {list(df.columns)}")

    # Convert wide-format (years as columns) to long-format (rows with 'year' and emission values)
    df_long = df.melt(id_vars=id_vars, var_name="year", value_name=value_name)
    df_long["year"] = df_long["year"].astype(int)

    # Fix VARCHAR(5) issue (truncate to 15 characters)
    df_long["edgar_country_code"] = df_long["edgar_country_code"].astype(str).str[:15]

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    # Insert rows into the table
    placeholders = ", ".join(["%s"] * len(df_long.columns))
    columns = ", ".join(df_long.columns)
    sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    for _, row in df_long.iterrows():
        cur.execute(sql_query, tuple(row))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Data successfully inserted into {table_name}.")

# Insert all datasets
insert_data_to_db("cleaned_ghg_totals.csv", "ghg_totals", ["edgar_country_code", "country"], "emission_value")
insert_data_to_db("cleaned_ghg_by_sector.csv", "ghg_sector_data", ["substance", "sector", "edgar_country_code", "country"], "emission_value")
insert_data_to_db("cleaned_ghg_per_gdp.csv", "ghg_per_gdp", ["edgar_country_code", "country"], "emission_per_gdp")
insert_data_to_db("cleaned_ghg_per_capita.csv", "ghg_per_capita", ["edgar_country_code", "country"], "emission_per_capita")
