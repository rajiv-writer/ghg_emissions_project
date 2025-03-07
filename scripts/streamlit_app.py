import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from sqlalchemy import create_engine

# Database credentials
DB_NAME = "ghg_emissions"
DB_USER = "postgres"
DB_PASS = "pwd333"
DB_HOST = "localhost"
DB_PORT = "5432"

# Create a database connection
def get_db_connection():
    return create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = get_db_connection()

# Load GHG Totals Data
def load_ghg_totals():
    query = """
    SELECT country, year, emission_value FROM ghg_totals
    WHERE year >= 1990
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# Load GHG per Capita & GDP Data
def load_ghg_per_capita_gdp():
    query = """
    SELECT country, year, emission_per_gdp, emission_per_capita FROM ghg_per_gdp
    JOIN ghg_per_capita USING (country, year)
    WHERE year >= 1990
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# Streamlit UI
st.set_page_config(layout="wide", page_title="🌍 GHG Emissions Dashboard", page_icon="🌎")
st.title("🌍 Global Greenhouse Gas Emissions Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_year = st.sidebar.slider("Select Year", min_value=1990, max_value=2023, value=2023)

# Load Data
ghg_df = load_ghg_totals()
ghg_per_capita_gdp_df = load_ghg_per_capita_gdp()

# Global Emissions Trend
st.subheader("📈 Global Green House Gas Emissions Over Time")
global_trend = ghg_df.groupby("year")["emission_value"].sum().reset_index()
fig1 = px.line(global_trend, x="year", y="emission_value", title="Global GHG Emissions")
st.plotly_chart(fig1, use_container_width=True)

# Country Comparison
top_countries = ghg_df[ghg_df["year"] == selected_year].nlargest(10, "emission_value")
st.subheader(f"🏆 Top 10 Emitting Countries in {selected_year}")
fig2 = px.bar(top_countries, x="country", y="emission_value", title=f"Top 10 Emitters in {selected_year}")
st.plotly_chart(fig2, use_container_width=True)

# Scatter Plot: GHG per Capita vs. GDP
st.subheader("📊 GHG Emissions Per Capita vs GDP")
# Filter data for the selected year and drop NaN values in emission_per_capita
filtered_df = ghg_per_capita_gdp_df[ghg_per_capita_gdp_df["year"] == selected_year].dropna(subset=["emission_per_capita", "emission_per_gdp"])

# Check if the filtered DataFrame is empty
if not filtered_df.empty:
    fig3 = px.scatter(
        filtered_df,
        x="emission_per_gdp", y="emission_per_capita",
        hover_name="country", size="emission_per_capita",
        title=f"GHG Emissions Per Capita vs GDP in {selected_year}")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning(f"No data available for {selected_year}. Please select another year.")


# World Map Visualization
st.subheader("🗺️ Global GHG Emissions Map")
world = gpd.read_file("D:/ghg_emissions_project/data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
print(world.columns)
merged = world.merge(ghg_df[ghg_df["year"] == selected_year], left_on="ADMIN", right_on="country", how="left")
fig4 = px.choropleth(merged, locations="ADM0_A3", color="emission_value", hover_name="country",
                      title=f"Global GHG Emissions in {selected_year}", projection="natural earth")
st.plotly_chart(fig4, use_container_width=True)

st.write("📌 *Data sourced from the EDGAR Database*")
