![gaspricewatcher_logo](./images/gaspricewatcher.png)

# Streamlit App
This application is created as part of the **Streamlit Connections Hackathon 🎉** [contest](https://discuss.streamlit.io/t/connections-hackathon/47574). The goal of this app is to demonstrate how to easily set up and retrieve data from one of my favorite data **APIs** (Application Programming Interfaces) – the public datasets from the *U.S. Bureau of Labor Statistics* (BLS) – by utilizing a custom-built **Streamlit** connection 🔌. This allows you to query the dataset(s) and save them as [pandas](https://pandas.pydata.org/) dataframes, providing a more user-friendly approach compared to the original Python code from BLS, which can be found [here](https://www.bls.gov/developers/api_python.htm#python2).

##Features

- Display data retrieved from the BLS API in a user-friendly manner using Streamlit.
- Visualize datasets with interactive charts and plots.
- Allow users to customize input parameters for data retrieval.

# Streamlit Connection API
The Streamlit Connection API is a custom-built Python package that allows you to easily interact with the U.S. Bureau of Labor Statistics (BLS) API and retrieve data as pandas dataframes.

## Installation

To install the Streamlit Connection API, simply run the following command:
```python
pip install streamlit_bls_connection
```

## Example Streamlit API:

```python
# Step 0: Install the package
pip install streamlit_bls_connection

import streamlit as st
from bls_connection import BLSConnection

# Step 1: Setup connection to US Bureau of Labor Statistics
connection = BLSConnection("bls_connection")

# Step 2: Define Input parameters for the API call
# Tip: one or multiple Series ID's* can be retrieved
seriesids_list = ['APU000074714', 'APU000072610']
start_year_str = '2014'  # start of date range
end_year_str = '2023'    # end of date range

# Step 3: Fetch data using the custom connection
dataframes_dict = connection.query(seriesids_list, start_year_str, end_year_str)

# Step 4: Create dataframes
gas_df = dataframes_dict['APU000074714']
electricity_df = dataframes_dict['APU000072610']

# Step 5: Show Dataframes in Streamlit
st.dataframe(gas_df, electricity_df)
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.