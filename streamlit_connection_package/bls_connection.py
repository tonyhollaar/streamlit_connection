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

    def fetch_data(self, seriesids, start_year, end_year):
        dataframes_dict = {}
        headers = {'Content-type': 'application/json'}
        
        # iterate over one or more timeseries
        for series_id in seriesids:
            # create empty list to save data for the current seriesId
            parsed_data = []
            # set the variable to retrieve from the public dataset
            data = json.dumps({"seriesid": [series_id], "startyear": start_year, "endyear": end_year})
            p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
            json_data = json.loads(p.text)
    
            # iterate over the json file
            for series in json_data['Results']['series']:
                # iterate over the list of lists that contains the data
                for item in series['data']:
                    # within each list retrieve the year, period, value and footnotes
                    year = item['year']
                    period = item['period']
                    value = item['value']
                    footnotes = ""
                    for footnote in item['footnotes']:
                        if footnote:
                            footnotes = footnotes + footnote['text'] + ','
                    parsed_data.append([series_id, year, period, value, footnotes[0:-1]])
    
            df = pd.DataFrame(parsed_data, columns=['seriesID', 'year', 'period', 'value', 'footnotes'])
            df['value'] = pd.to_numeric(df['value'])
            df['month'] = pd.to_numeric(df['period'].replace({'M': ''}, regex=True))
            df['date'] = df['month'].map(str) + '-' + df['year'].map(str)
            df['date'] = pd.to_datetime(pd.to_datetime(df['date'], format='%m-%Y').dt.strftime('%m-%Y'))
            df = df.sort_values(by='date', ascending=True)
            df['perct_change_value'] = df['value'].pct_change()
    
            # add the dataframe to the dictionary with the seriesid as the key
            dataframes_dict[series_id] = df
        return dataframes_dict
    
    @staticmethod
    @st.cache_data(ttl="1d")  # Cache the data for one day (24 hours)
    def query(series_id, start_year, end_year):
        # This method will be called by the Streamlit app to retrieve data using the custom connection.
        # You can implement any caching logic or other data processing here.
        connection = BLSConnection("bls_connection")
        try:
            return connection.fetch_data(series_id, start_year, end_year)
        except KeyError:
            with st.sidebar:
                st.error("😒 **Error**: Failed to fetch latest data. Daily query limit is exceeded, retrieving stored data from backup source.")
           #st.stop()  # Stop the app execution and display the error message to the user
            return None