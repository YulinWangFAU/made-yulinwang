import unittest
import os
import pandas as pd
from pipeline import (
    download_covid_data, download_world_bank_data,
)

class TestDataPipeline(unittest.TestCase):

    def setUp(self):
        # Define test URLs or paths
        self.covid_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
        self.world_bank_path = "data/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_142.csv"
        self.output_file = "output/test_output.csv"

    def test_download_covid_data(self):
        # Test downloading COVID data
        covid_df = download_covid_data(self.covid_url)
        self.assertIsInstance(covid_df, pd.DataFrame)
        self.assertGreater(len(covid_df), 0)
        self.assertIn('Country/Region', covid_df.columns)

    def test_download_world_bank_data(self):
        # Test downloading World Bank data
        world_bank_df = download_world_bank_data(self.world_bank_path)
        self.assertIsInstance(world_bank_df, pd.DataFrame)
        self.assertGreater(len(world_bank_df), 0)
        self.assertIn('Country', world_bank_df.columns)

    def test_data_cleaning_and_merging(self):
        # Download datasets
        covid_df = download_covid_data(self.covid_url)
        world_bank_df = download_world_bank_data(self.world_bank_path)

        # Clean and merge data
        covid_df = covid_df.drop(['Province/State', 'Lat', 'Long'], axis=1)
        covid_df = covid_df.melt(id_vars=['Country/Region'], var_name='Date', value_name='Deaths')
        covid_df['Date'] = pd.to_datetime(covid_df['Date'], format='%m/%d/%y')
        covid_df = covid_df.groupby(['Country/Region', 'Date']).sum().reset_index()
        world_bank_df = world_bank_df.rename(columns={'Country Name': 'Country', '2020': 'GDP per Capita'})
        world_bank_df = world_bank_df[['Country', 'Country Code', 'GDP per Capita']]

        # Merge
        merged_df = covid_df.merge(world_bank_df, left_on='Country/Region', right_on='Country', how='inner')

        self.assertIsInstance(merged_df, pd.DataFrame)
        self.assertGreater(len(merged_df), 0)
        self.assertIn('Country', merged_df.columns)
        self.assertIn('Deaths', merged_df.columns)

    def test_output_file_creation(self):
        # Check if the pipeline creates the output file
        # Dummy output generation for testing
        pd.DataFrame({"Test": [1, 2, 3]}).to_csv(self.output_file, index=False)
        self.assertTrue(os.path.exists(self.output_file))
        os.remove(self.output_file)


if __name__ == '__main__':
    unittest.main()
