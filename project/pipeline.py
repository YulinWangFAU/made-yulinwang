import os
import sqlite3
import pandas as pd

# Directory setup
DATA_DIR = "./data"
PROJECT_DIR = "./project"
DATABASE_PATH = os.path.join(DATA_DIR, "database.sqlite")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PROJECT_DIR, exist_ok=True)

def download_data():
    """Download datasets and save them locally."""
    covid_data_url = "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
    socioeconomic_data_path = "/Users/wangyulin/MADE/made-yulinwang/data/socioeconomic_Data.csv"  # Local file path for socioeconomic data

    covid_data = pd.read_csv(covid_data_url)
    return covid_data, socioeconomic_data_path

def clean_covid_data(covid_data):
    """Clean and preprocess COVID-19 data, retaining year and month dimensions."""
    covid_data = covid_data.rename(columns={
        'location': 'country',
        'date': 'year'
    })
    covid_data['date'] = pd.to_datetime(covid_data['year'])
    covid_data['year'] = covid_data['date'].dt.year
    covid_data['month'] = covid_data['date'].dt.month

    americas_countries = [
        "Argentina", "Brazil", "Canada", "Chile", "Colombia", "Mexico", "United States", 
        "Peru", "Cuba", "Venezuela", "Ecuador", "Guatemala", "Honduras", "Paraguay", 
        "Uruguay", "Bolivia", "Panama", "Costa Rica"
    ]
    covid_data = covid_data[covid_data['country'].isin(americas_countries)]

    country_mapping = {
        "Bahamas, The": "Bahamas",
        "Venezuela, RB": "Venezuela",
    }
    covid_data["country"] = covid_data["country"].replace(country_mapping)

    covid_columns = [
        'country', 'date', 'year', 'month',
        'total_cases', 'total_deaths',
        'excess_mortality_cumulative_per_million', 'total_vaccinations_per_hundred',
        'icu_patients_per_million', 'hospital_beds_per_thousand', 'population'
    ]
    covid_data = covid_data[covid_columns]

    covid_monthly = covid_data.groupby(['country', 'year', 'month']).agg({
        'total_cases': 'max',
        'total_deaths': 'max',
        'excess_mortality_cumulative_per_million': 'max',
        'total_vaccinations_per_hundred': 'max',
        'icu_patients_per_million': 'max',
        'hospital_beds_per_thousand': 'max',
        'population': 'max'
    }).reset_index()

    return covid_monthly

def aggregate_covid_data(covid_monthly):
    """Aggregate COVID-19 data by year for merging with socioeconomic data."""
    covid_aggregated = covid_monthly.groupby(['country', 'year']).agg({
        'total_cases': 'max',
        'total_deaths': 'max',
        'excess_mortality_cumulative_per_million': 'mean',
        'total_vaccinations_per_hundred': 'mean',
        'icu_patients_per_million': 'mean',
        'hospital_beds_per_thousand': 'mean',
        'population': 'max'
    }).reset_index()

    return covid_aggregated

def clean_socioeconomic_data(file_path):
    """Clean, transform, and pivot socioeconomic data."""
    # Load the raw data
    raw_data = pd.read_csv(file_path)

    # Convert the data into a long format
    data_long = raw_data.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        var_name="year",
        value_name="indicator_value"
    )

    # Rename columns for clarity
    data_long.rename(columns={
        "Country Name": "country",
        "Series Name": "indicator_name",
    }, inplace=True)

    # Extract the year from the `year` column
    data_long["year"] = data_long["year"].str.extract("([0-9]{4})").astype(int)

    # Ensure `indicator_value` is numeric
    data_long["indicator_value"] = pd.to_numeric(data_long["indicator_value"], errors="coerce")

    # Select relevant indicators
    selected_indicators = [
        "GDP per capita (current US$)",
        "Life expectancy at birth, total (years)",
        "Unemployment, total (% of total labor force) (modeled ILO estimate)",
        "Gini index",
        "Current health expenditure (% of GDP)",
        "Domestic general government health expenditure per capita (current US$)",
        "Urban population (% of total population)",
        "Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)"
    ]
    data_filtered = data_long[data_long["indicator_name"].isin(selected_indicators)]

    # Filter for countries in the Americas
    americas_countries = [
        "Argentina", "Brazil", "Canada", "Chile", "Colombia", "Mexico", "United States", 
        "Peru", "Cuba", "Venezuela", "Ecuador", "Guatemala", "Honduras", "Paraguay", 
        "Uruguay", "Bolivia", "Panama", "Costa Rica"
    ]
    data_filtered = data_filtered[data_filtered["country"].isin(americas_countries)]

    # Map country names to standardized format
    country_mapping = {
        "Bahamas, The": "Bahamas",
        "Venezuela, RB": "Venezuela",
    }
    data_filtered["country"] = data_filtered["country"].replace(country_mapping)

    # Drop rows with missing or invalid values
    data_cleaned = data_filtered.dropna()

    # Pivot the data to make indicators as columns
    data_pivoted = data_cleaned.pivot_table(
        index=["country", "year"],  # Country and year as index
        columns="indicator_name",  # Indicators as columns
        values="indicator_value"   # Values
    ).reset_index()  # Reset index for easier merging

    return data_pivoted


def clean_and_merge_data(covid_data, socioeconomic_data_path):
    """Clean and merge COVID-19 and socioeconomic data, with monthly and yearly aggregation."""
    covid_monthly = clean_covid_data(covid_data)

    covid_aggregated = aggregate_covid_data(covid_monthly)

    socioeconomic_data = clean_socioeconomic_data(socioeconomic_data_path)

    merged_data = pd.merge(covid_aggregated, socioeconomic_data, on=["country", "year"], how="outer")

    merged_data.fillna(0, inplace=True)

    return covid_monthly, merged_data

def save_to_database(covid_monthly, merged_data):
    """Save cleaned data to SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)

    covid_monthly.to_sql("covid_monthly", connection, if_exists="replace", index=False)
    merged_data.to_sql("merged_data", connection, if_exists="replace", index=False)

    connection.close()

    print("Data saved to database at", DATABASE_PATH)

def main():
    covid_data, socioeconomic_data_path = download_data()

    covid_monthly, merged_data = clean_and_merge_data(covid_data, socioeconomic_data_path)

    save_to_database(covid_monthly, merged_data)

if __name__ == "__main__":
    main()
