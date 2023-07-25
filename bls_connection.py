# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:12:23 2023

@author: tholl
"""
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import requests
import pandas as pd
import json

class BLSConnection(ExperimentalBaseConnection):
    def __init__(self, connection_name, **kwargs):
        super().__init__(connection_name=connection_name, **kwargs)
        # Load any connection-specific configuration or credentials here if needed.

    def _connect(self, **kwargs):
        # Implement the connection setup here.
        # We don't need to explicitly set up a connection in this case,
        # as we'll be making direct API calls in the methods below.
        pass

    def fetch_data(self, series_id, start_year, end_year):
        # Make the API call to the BLS API and fetch the data
        url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
        headers = {'Content-type': 'application/json'}
        data = json.dumps({"seriesid": [series_id], "startyear": start_year, "endyear": end_year})
        response = requests.post(url, data=data, headers=headers)
        json_data = json.loads(response.text)

        # Process the API response and create a DataFrame
        parsed_data = []
        for series in json_data['Results']['series']:
            seriesId = series['seriesID']
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                footnotes = ""
                for footnote in item['footnotes']:
                    if footnote:
                        footnotes = footnotes + footnote['text'] + ','
                parsed_data.append([seriesId, year, period, value, footnotes[0:-1]])

        df = pd.DataFrame(parsed_data, columns=['seriesID', 'year', 'period', 'value', 'footnotes'])
        df['value'] = pd.to_numeric(df['value'])
        df['month'] = pd.to_numeric(df['period'].replace({'M': ''}, regex=True))
        df['date'] = df['month'].map(str) + '-' + df['year'].map(str)
        df['date'] = pd.to_datetime(pd.to_datetime(df['date'], format='%m-%Y').dt.strftime('%m-%Y'))
        df = df.sort_values(by=['year', 'month'], ascending=True)
        df['perct_change_value'] = df['value'].pct_change() * 100
        df['perct_change_value'] = df['perct_change_value'].shift(-1)  # Shift the percentage change by one row

        return df
    
    @staticmethod
    @st.cache_data(ttl="1d")  # Cache the data for one day (24 hours)
    def query(series_id, start_year, end_year):
        # This method will be called by the Streamlit app to retrieve data using the custom connection.
        # You can implement any caching logic or other data processing here.
        connection = BLSConnection("bls_connection")
        try:
            return connection.fetch_data(series_id, start_year, end_year)
        except KeyError:
# =============================================================================
#             with st.sidebar:
#                 st.error("😒 **Error**: Failed to fetch latest data. Daily query limit is exceeded, retrieving stored data from backup source.")
# =============================================================================
           #st.stop()  # Stop the app execution and display the error message to the user
            return None