import json
import os
import requests
import numpy as np
import pandas as pd
import sqlalchemy as sql
from io import StringIO
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.impute import KNNImputer

def extract_csv_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("CSV file downloaded successfully.")
        csv_data = StringIO(response.content.decode('utf-8'))
        df = pd.read_csv(csv_data, encoding='latin1')
        return df
    else:
        print(f"Failed to retrieve data from {url}, status code: {response.status_code}")
        return None

def create_sqlite_database(database_name):
    data_directory = './data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    database_path = os.path.join(data_directory, database_name)
    if os.path.exists(database_path):
        os.remove(database_path)

    engine = sql.create_engine(f'sqlite:///{database_path}')
    return engine

def filter_americas(df, column_name='Country'):
    americas_countries = [
        "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Canada", "Chile", "Colombia", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "Ecuador", "El Salvador", "Grenada", "Guatemala", "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Suriname", "Trinidad and Tobago", "United States", "Uruguay", "Venezuela"
    ]
    return df[df[column_name].isin(americas_countries)]

def main():
    # COVID-19 Mortality Data
    covid_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    df_covid = extract_csv_data(covid_url)
    df_covid = df_covid.drop(['Province/State', 'Lat', 'Long'], axis=1)
    df_covid = df_covid.melt(id_vars=['Country/Region'], var_name='Date', value_name='Deaths')
    df_covid['Date'] = pd.to_datetime(df_covid['Date'], format='%m/%d/%y')
    df_covid = df_covid.groupby(['Country/Region', 'Date']).sum().reset_index()

    # Filter COVID-19 data for Americas
    df_covid = filter_americas(df_covid, column_name='Country/Region')

    # World Bank Data
    world_bank_url = "data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_142.csv"
    df_world_bank = pd.read_csv(world_bank_url, skiprows=4)
    df_world_bank = df_world_bank.rename(columns={'Country Name': 'Country', '2020': 'GDP per Capita'})
    df_world_bank = df_world_bank[['Country', 'Country Code', 'GDP per Capita']]

    # Additional World Bank Data
    healthcare_expenditure_url = "data/API_SH.XPD.CHEX.GD.ZS_DS2_en_csv_v2_4879.csv"
    df_healthcare = pd.read_csv(healthcare_expenditure_url, skiprows=4)
    df_healthcare = df_healthcare.rename(columns={'Country Name': 'Country', '2020': 'Healthcare Expenditure Per Capita'})
    df_healthcare = df_healthcare[['Country', 'Healthcare Expenditure Per Capita']]

    urbanization_url = "data/API_SP.URB.TOTL_DS2_en_csv_v2_976.csv"
    df_urbanization = pd.read_csv(urbanization_url, skiprows=4)
    df_urbanization = df_urbanization.rename(columns={'Country Name': 'Country', '2020': 'Urbanization Rate'})
    df_urbanization = df_urbanization[['Country', 'Urbanization Rate']]

    population_density_url = "data/API_EN.POP.DNST_DS2_en_csv_v2_1002.csv"
    df_population_density = pd.read_csv(population_density_url, skiprows=4)
    df_population_density = df_population_density.rename(columns={'Country Name': 'Country', '2020': 'Population Density'})
    df_population_density = df_population_density[['Country', 'Population Density']]

    # Filter World Bank data for Americas
    df_world_bank = filter_americas(df_world_bank)
    df_healthcare = filter_americas(df_healthcare)
    df_urbanization = filter_americas(df_urbanization)
    df_population_density = filter_americas(df_population_density)

    # Merge World Bank Data
    df_world_bank = df_world_bank.merge(df_healthcare, on='Country', how='left')
    df_world_bank = df_world_bank.merge(df_urbanization, on='Country', how='left')
    df_world_bank = df_world_bank.merge(df_population_density, on='Country', how='left')

    # Merge all datasets
    df_covid = df_covid.merge(df_world_bank, left_on='Country/Region', right_on='Country', how='left')

    # Create SQLite Database
    engine = create_sqlite_database('database.sqlite')

    # Save to SQLite
    df_covid.to_sql('covid_deaths', con=engine, index=False)
    df_world_bank.to_sql('world_bank_data', con=engine, index=False)

    print("Data pipeline executed and stored in database.sqlite successfully.")

if __name__ == "__main__":
    main()
