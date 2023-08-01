# -*- coding: utf-8 -*-
"""                                                                                                                                                                                               
Created on Mon Jul 24 15:12:23 2023
@author: tonyhollaar
"""
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import requests
import pandas as pd
import json

class BLSConnection(ExperimentalBaseConnection):
    def __init__(self, connection_name, **kwargs):
        """
        Initializes the BLSConnection object.
        
        Parameters:
        ----------
        connection_name : str
            A name for the connection.
        **kwargs : keyword arguments, optional
            Additional keyword arguments that can be passed to the parent class constructor.
        
        Returns:
        -------
        None
        """
        super().__init__(connection_name=connection_name, **kwargs)
        
    def _connect(self, **kwargs):
        # Implement the connection setup here.
        # We don't need to explicitly set up a connection in this case,
        # as we'll be making direct API calls in the methods below.
        pass

    def fetch_data(self, seriesids, start_year, end_year, api_key=None, **kwargs):
        """
        Fetches data from the Bureau of Labor Statistics (BLS) API and returns it as a dictionary of DataFrames.
        
        Parameters:
        ----------
        seriesids : list of str
            The series IDs representing the BLS time series data to fetch. Each ID should be a string.
        start_year : str
            The start year for the data retrieval (inclusive), represented as a string.
        end_year : str
            The end year for the data retrieval (inclusive), represented as a string.
        api_key : str, optional
            The API key for accessing the BLS API. If not provided, some restrictions may apply to the data retrieval.
            Note: Without an API key, you might be subject to limitations on the number of requests you can make.
        **kwargs : keyword arguments, optional
            Additional keyword arguments to customize the data retrieval.
            Possible keyword arguments include:
            - catalog : bool, optional
                Whether to include catalog data for the series. Default is False.
            - calculations : bool, optional
                Whether to include calculated data for the series. Default is False.
            - annualaverage : bool, optional
                Whether to include annual average data for the series. Default is False.
            - aspects : bool, optional
                Whether to include additional aspects data for the series. Default is False.
        
        Returns:
        -------
        dict of DataFrame(s)
            A dictionary with series IDs as keys and DataFrames as values, containing the fetched BLS data for each series.
            Each DataFrame includes columns for 'date', 'value', '%_change_value', 'year', 'month', 'period'.
            If the API key is provided, 'seriesID', 'series_title', and 'survey_name' columns are also included in the DataFrames.
            Empty or all-None columns are excluded from the DataFrames.
        """
        dataframes_dict = {}
        headers = {
            'Content-type': 'application/json',
        }
    
        # Build the payload with required parameters
        payload = {
            "seriesid": seriesids,
            "startyear": start_year,
            "endyear": end_year,
            "registrationkey": api_key
        }
    
        # Update the payload with additional parameters from **kwargs
        payload.update(kwargs)
    
        # Make the API request using the POST method with the payload
        p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', json=payload, headers=headers)
        json_data = json.loads(p.text)
        
        # Iterate over the JSON response and extract data for each series
        for series in json_data['Results']['series']:
            series_id = series['seriesID']
            parsed_data = []
    
            # Extract catalog data for the current series if available
            series_title = series.get('catalog', {}).get('series_title')
            survey_name = series.get('catalog', {}).get('survey_name')
    
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                footnotes = ",".join(footnote['text'] for footnote in item['footnotes'] if footnote)
    
                # Create a dictionary with the common data fields
                row_data = {
                    'seriesID': series_id,
                    'year': year,
                    'period': period,
                    'value': value,
                    'footnotes': footnotes,
                    'series_title': series_title,
                    'survey_name': survey_name,
                    'catalog': series.get('catalog'),
                    'calculations': item.get('calculations'),
                    'annualaverage': item.get('annualaverage'),
                    'aspects': item.get('aspects')
                }
    
                parsed_data.append(row_data)
    
            # Create DataFrame for the current series
            columns = ['seriesID', 'series_title', 'survey_name', 'year', 'period', 'value', 'catalog', 'calculations', 'annualaverage', 'aspects', 'footnotes']
            data = [[entry.get(i, None) for i in columns] for entry in parsed_data]
            df = pd.DataFrame(data, columns=columns)
    
            df['value'] = pd.to_numeric(df['value'])
            df['month'] = pd.to_numeric(df['period'].replace({'M': ''}, regex=True))
            df['date'] = pd.to_datetime(df['month'].map(str) + '-' + df['year'].map(str), format='%m-%Y')
            df = df.sort_values(by='date', ascending=True)
            df['%_change_value'] = df['value'].pct_change()
    
            # Reorder the columns in the DataFrame
            df = df[['date', 'value', '%_change_value', 'seriesID', 'series_title', 'year', 'month', 'period', 'survey_name', 'catalog', 'calculations', 'annualaverage', 'aspects', 'footnotes']]
    
            # Reset the index to start from 0
            df.reset_index(drop=True, inplace=True)
    
            # Replace empty strings with NaN
            df.replace('', pd.NA, inplace=True)
            
            # Drop columns where all values are either NaN or pd.NA
            df = df.dropna(axis=1, how='all')
    
            # Add the DataFrame to the dictionary with the seriesid as the key
            dataframes_dict[series_id] = df
    
        return dataframes_dict
    
    @classmethod
    @st.cache_data(ttl="1d")  # Cache the data for one day (24 hours)
    def query(cls, seriesids, start_year, end_year, api_key=None, **kwargs):
        """
        Fetches data from the Bureau of Labor Statistics (BLS) API.
        
        Parameters:
        ----------
        seriesids : list of str
            The series IDs representing the BLS time series data to fetch. Each ID should be a string.
        start_year : str
            The start year for the data retrieval (inclusive), represented as a string.
        end_year : str
            The end year for the data retrieval (inclusive), represented as a string.
        api_key : str, optional
            The API key for accessing the BLS API. If not provided, some restrictions may apply to the data retrieval.
            Note: Without an API key, you might be subject to limitations on the number of requests you can make.
        **kwargs : keyword arguments, optional
            Additional keyword arguments to customize the data retrieval.
            Possible keyword arguments include:
            - catalog : bool, optional
                Whether to include catalog data for the series. Default is False.
            - calculations : bool, optional
                Whether to include calculated data for the series. Default is False.
            - annualaverage : bool, optional
                Whether to include annual average data for the series. Default is False.
            - aspects : bool, optional
                Whether to include additional aspects data for the series. Default is False.

        Returns:
        -------
        dict of DataFrame(s)
            A dictionary with series IDs as keys and DataFrames as values, containing the fetched BLS data for each series.
            Each DataFrame includes columns for 'date', 'value', '%_change_value', 'year', 'month', 'period'.
            If the API key is provided, 'seriesID','series_title' and 'survey_name' and **kwargs columns are also included in the DataFrames.
            Empty or all-None columns are excluded from the DataFrames.
                
        Example:
        --------
        # Setup connection
        conn = st.experimental_connection('bls', type=BLSConnection)
   
        # Set your API key obtained from https://data.bls.gov/registrationEngine/
        api_key = 'YOUR_API_KEY_HERE'  # Replace with your key or set to None.
        
        # Optionally, store the API key in secrets.toml under [connections_bls] with api_key = 'YOUR_KEY'
        # and set api_key = st.secrets["connections_bls"]["api_key"] to use it securely.

        # Calling the query method with additional keyword arguments
        dataframes_dict = conn.query(
            seriesids=seriesids_list = ['APU000074714', 'APU000074715'],
            start_year= '2014',
            end_year= '2023',
            api_key=api_key,
            catalog=True,
            calculations=True,
            annualaverage=True,
            aspects=True
        )
   
        # Access the retrieved DataFrames using the 'dataframes_dict' dictionary.
        first_series_dataframe = dataframes_dict[seriesids_list[0]]  # DataFrame for the first series ID.
        
        # Alternatively, access the first DataFrame using its series ID.
        first_series_dataframe = dataframes_dict['APU000074714']
        """
        try:
            # This method will be called by the Streamlit app to retrieve data using the custom connection.
            # You can implement any caching logic or other data processing here.
            connection = cls("bls_connection")
        
            # Fetch data using the custom connection
            dataframes_dict = connection.fetch_data(
                seriesids=seriesids,
                start_year=start_year,
                end_year=end_year,
                api_key=api_key,  # Pass the api_key or set to None
                **kwargs          # Pass any additional keyword arguments
            )
            return dataframes_dict
        except KeyError:
            with st.sidebar:
                st.error("😒 **Error**: Failed to fetch latest data. Daily query limit is exceeded.")
            return None

