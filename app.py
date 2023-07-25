# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:16:06 2023

@author: tholl
"""
import streamlit as st

# Data Packages
import pandas as pd
from pandas.core.dtypes.dtypes import dtypes
import math
import numpy as np
import json
import requests
import re

# Visualization Packages
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import pyplot
import plotly.express as px
import seaborn as sns



def web_scrape_public_dataset(series_id, start_year, end_year):
    # Create empty list to save data to
    parsed_data = []

    # Source: https://www.bls.gov/developers/api_python.htm#python2
    headers = {'Content-type': 'application/json'}

    # Set the variables to retrieve from public dataset
    data = json.dumps({"seriesid": [series_id], "startyear": start_year, "endyear": end_year})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    # Iterate over the JSON file
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        # Iterate over the list of lists that contains the data
        for item in series['data']:
            # Within each list, retrieve the year, period, value, and footnotes
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes = ""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
            parsed_data.append([seriesId, year, period, value, footnotes[0:-1]])

    # Convert JSON data into a pandas dataframe
    df = pd.DataFrame(parsed_data, columns=['seriesID', 'year', 'period', 'value', 'footnotes'])

    # Change datatype for the 'value' column to numeric
    df['value'] = pd.to_numeric(df['value'])

    # Change the 'period' to integer value as numeric datatype
    df['month'] = pd.to_numeric(df['period'].replace({'M': ''}, regex=True))

    # Add date column
    df['date'] = df['month'].map(str) + '-' + df['year'].map(str)
    df['date'] = pd.to_datetime(pd.to_datetime(df['date'], format='%m-%Y').dt.strftime('%m-%Y'))

    # Add percent change column e.g., 1 equals 1%
    df['perct_change_value'] = df['value'].pct_change() * 100

    # Sort the dataframe from oldest to newest value
    df = df.sort_values(by=['year', 'month'], ascending=True)

    return df

series_id = 'APU000074714'
start_year = '2018'
end_year = '2023'
data_df = web_scrape_public_dataset(series_id, start_year, end_year)



