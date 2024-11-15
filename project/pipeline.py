# Import necessary libraries
import pandas as pd
import numpy as np
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point

# Step 1: Data Collection and Cleaning
def download_covid_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        csv_data = StringIO(response.content.decode('utf-8'))
        covid_df = pd.read_csv(csv_data)
        return covid_df
    else:
        raise ValueError(f"Failed to download data from {url}, status code: {response.status_code}")

def download_world_bank_data(url):
    # Assuming you have already downloaded the World Bank CSV data to a local file
    try:
        world_bank_df = pd.read_csv(url, skiprows=4)
        return world_bank_df
    except pd.errors.ParserError as e:
        raise ValueError(f"Error reading the World Bank CSV file: {e}")

# URLs
covid_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
world_bank_url = "data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_142.csv"  # Local path

# Download datasets
covid_df = download_covid_data(covid_url)
world_bank_df = download_world_bank_data(world_bank_url)

# Data Cleaning
# Cleaning COVID-19 dataset
covid_df = covid_df.drop(['Province/State', 'Lat', 'Long'], axis=1)
covid_df = covid_df.melt(id_vars=['Country/Region'], var_name='Date', value_name='Deaths')
covid_df['Date'] = pd.to_datetime(covid_df['Date'], format='%m/%d/%y')
covid_df = covid_df.groupby(['Country/Region', 'Date']).sum().reset_index()

# Cleaning World Bank dataset
world_bank_df = world_bank_df.rename(columns={'Country Name': 'Country', '2020': 'GDP per Capita'})
world_bank_df = world_bank_df[['Country', 'Country Code', 'GDP per Capita']]

# Standardizing country names for merging
country_mapping = {
    "United States": "US",
    "Russian Federation": "Russia",
    "Korea, Rep.": "South Korea"
    # Add more as necessary for alignment
}
world_bank_df['Country'] = world_bank_df['Country'].replace(country_mapping)

# Filter for countries in the Americas (North, Central, and South America, and the Caribbean)
americas_countries = [
    "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil", "Canada", "Chile", "Colombia", "Costa Rica", 
    "Cuba", "Dominica", "Dominican Republic", "Ecuador", "El Salvador", "Grenada", "Guatemala", "Guyana", 
    "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Saint Kitts and Nevis", 
    "Saint Lucia", "Saint Vincent and the Grenadines", "Suriname", "Trinidad and Tobago", "United States", "Uruguay", "Venezuela"
]

world_bank_df = world_bank_df[world_bank_df['Country'].isin(americas_countries)]
covid_df = covid_df[covid_df['Country/Region'].isin(americas_countries)]

# Adding region information (North America, Central America, South America, Caribbean)
region_mapping = {
    "Canada": "North America",
    "United States": "North America",
    "Mexico": "North America",
    "Belize": "Central America",
    "Costa Rica": "Central America",
    "El Salvador": "Central America",
    "Guatemala": "Central America",
    "Honduras": "Central America",
    "Nicaragua": "Central America",
    "Panama": "Central America",
    "Argentina": "South America",
    "Bolivia": "South America",
    "Brazil": "South America",
    "Chile": "South America",
    "Colombia": "South America",
    "Ecuador": "South America",
    "Guyana": "South America",
    "Paraguay": "South America",
    "Peru": "South America",
    "Suriname": "South America",
    "Uruguay": "South America",
    "Venezuela": "South America",
    "Bahamas": "Caribbean",
    "Barbados": "Caribbean",
    "Cuba": "Caribbean",
    "Dominica": "Caribbean",
    "Dominican Republic": "Caribbean",
    "Grenada": "Caribbean",
    "Haiti": "Caribbean",
    "Jamaica": "Caribbean",
    "Saint Kitts and Nevis": "Caribbean",
    "Saint Lucia": "Caribbean",
    "Saint Vincent and the Grenadines": "Caribbean",
    "Trinidad and Tobago": "Caribbean"
}

world_bank_df['Region'] = world_bank_df['Country'].map(region_mapping)
merged_df = covid_df.merge(world_bank_df, left_on='Country/Region', right_on='Country', how='inner')

# Step 2: Exploratory Data Analysis (EDA)
def exploratory_data_analysis(df):
    # Summarize key variables
    print(df.describe())
    
    # GDP vs Mortality Scatter Plot
    latest_data = df[df['Date'] == df['Date'].max()]
    plt.figure(figsize=(16, 10))
    sns.scatterplot(data=latest_data, x='GDP per Capita', y='Deaths', hue='Region', s=100, alpha=0.7, edgecolor='w', linewidth=0.5)
    for i in range(len(latest_data)):
        plt.text(latest_data['GDP per Capita'].iloc[i], latest_data['Deaths'].iloc[i], 
                 latest_data['Country'].iloc[i], fontsize=9, ha='right', va='bottom', alpha=0.8)
    plt.title('GDP per Capita vs COVID-19 Deaths in the Americas', fontsize=16)
    plt.xlabel('GDP per Capita (USD)', fontsize=14)
    plt.ylabel('Total Deaths', fontsize=14)
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.tight_layout()
    plt.show()

    # Boxplot for GDP categories
    bins = [0, 5000, 15000, 50000]
    labels = ['Low', 'Medium', 'High']
    latest_data['GDP Category'] = pd.cut(latest_data['GDP per Capita'], bins=bins, labels=labels)
    plt.figure(figsize=(14, 8))
    sns.boxplot(x='GDP Category', y='Deaths', data=latest_data, hue='Region', palette='Set2')
    plt.title('COVID-19 Deaths by GDP Category in the Americas', fontsize=16)
    plt.xlabel('GDP Category', fontsize=14)
    plt.ylabel('Total Deaths', fontsize=14)
    plt.tight_layout()
    plt.show()

exploratory_data_analysis(merged_df)

# Step 3: Statistical Analysis
def correlation_analysis(df):
    # Extract latest available data for correlation
    latest_data = df[df['Date'] == df['Date'].max()]
    latest_data_numeric = latest_data.select_dtypes(include=[np.number])
    correlation = latest_data_numeric.corr()
    print("Correlation between GDP per Capita and Deaths in the Americas:")
    print(correlation)

    # Simple regression
    sns.lmplot(data=latest_data, x='GDP per Capita', y='Deaths', hue='Region', aspect=1.5, height=8)
    plt.title('Linear Regression: GDP per Capita vs COVID-19 Deaths in the Americas', fontsize=16)
    plt.xlabel('GDP per Capita (USD)', fontsize=14)
    plt.ylabel('Total Deaths', fontsize=14)
    plt.tight_layout()
    plt.show()

correlation_analysis(merged_df)

# Step 4: Reporting and Visualization
def create_visualizations(df):
    # Heatmap of correlation matrix
    numeric_df = df.select_dtypes(include=[np.number])
    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap for the Americas')
    plt.show()

    # Mortality rate per GDP
    df['Mortality Rate per GDP'] = df['Deaths'] / df['GDP per Capita']
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Country', y='Mortality Rate per GDP', hue='Region', data=df.sort_values('Mortality Rate per GDP', ascending=False).head(10))
    plt.xticks(rotation=45)
    plt.title('Top 10 Countries in the Americas with Highest Mortality Rate per GDP')
    plt.xlabel('Country')
    plt.ylabel('Mortality Rate per Unit of GDP')
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    # Map Visualization of COVID-19 Deaths
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    americas = world[world['continent'].isin(['North America', 'South America'])]
    merged_df_geo = df.merge(americas, left_on='Country/Region', right_on='name')
    geo_df = gpd.GeoDataFrame(merged_df_geo, geometry='geometry')
    fig, ax = plt.subplots(figsize=(15, 15))
    americas.plot(ax=ax, color='lightgrey')
    geo_df.plot(ax=ax, column='Deaths', markersize=geo_df['Deaths'] / 1000, legend=True, alpha=0.5)
    plt.title('COVID-19 Deaths in the Americas')
    plt.show()

create_visualizations(merged_df)
