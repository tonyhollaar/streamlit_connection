# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:13:46 2023
@author: tholl
data source: https://data.bls.gov/timeseries/APU000074714
"""
# =============================================================================
#   _      _____ ____  _____            _____  _____ ______  _____ 
#  | |    |_   _|  _ \|  __ \     /\   |  __ \|_   _|  ____|/ ____|
#  | |      | | | |_) | |__) |   /  \  | |__) | | | | |__  | (___  
#  | |      | | |  _ <|  _  /   / /\ \ |  _  /  | | |  __|  \___ \ 
#  | |____ _| |_| |_) | | \ \  / ____ \| | \ \ _| |_| |____ ____) |
#  |______|_____|____/|_|  \_\/_/    \_\_|  \_\_____|______|_____/ 
#                                                                  
# =============================================================================
import streamlit as st
import pandas as pd
from datetime import datetime
from bls_connection import BLSConnection
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json
import base64
from fire_state import create_store, form_update, get_state, set_state, get_store, set_store


# =============================================================================
#   _____        _____ ______    _____ ______ _______ _    _ _____  
#  |  __ \ /\   / ____|  ____|  / ____|  ____|__   __| |  | |  __ \ 
#  | |__) /  \ | |  __| |__    | (___ | |__     | |  | |  | | |__) |
#  |  ___/ /\ \| | |_ |  __|    \___ \|  __|    | |  | |  | |  ___/ 
#  | |  / ____ \ |__| | |____   ____) | |____   | |  | |__| | |     
#  |_| /_/    \_\_____|______| |_____/|______|  |_|   \____/|_|     
#                                                                                                                                    
# =============================================================================
# SET PAGE CONFIGURATIONS STREAMLIT
st.set_page_config(page_title = "GASPRICEWATCHER", 
                   layout = "centered", # "centered" or "wide"
                   page_icon = "🛢️", 
                   initial_sidebar_state = "expanded") # "auto" or "expanded" or "collapsed"

# SET FONT STYLE(S)
font_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Ysabeau+SC:wght@200&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');
            /* Set the font family for header elements */
            h2 {
                font-family: 'Lobster', cursive;
            }
            /* Set the font family for paragraph elements */
            p {
               font-family: 'Ysabeau SC', sans-serif;
            }
            
            /* Set the font family, size, and weight for unordered list and ordered list elements */
            ul, ol {
                font-family: 'Ysabeau SC', sans-serif;
                font-size: 16px;
                font-weight: normal;
            }
            
            /* Set the font family, size, weight, and margin for list item elements */
            li {
                font-family: 'Ysabeau SC', sans-serif;
                font-size: 16px;
                font-weight: normal;
                margin-top: 5px;
            }
            </style>
            """
# APPLY FONTSTYLE(S)            
st.markdown(font_style, unsafe_allow_html=True)

# Define the font size of the st.metric
st.markdown("""
            <style>
            [data-testid="stMetricValue"] {
                font-size: 36px;
            }
            </style>
            """, unsafe_allow_html=True)

# =============================================================================
#   ______ _    _ _   _  _____ _______ _____ ____  _   _  _____ 
#  |  ____| |  | | \ | |/ ____|__   __|_   _/ __ \| \ | |/ ____|
#  | |__  | |  | |  \| | |       | |    | || |  | |  \| | (___  
#  |  __| | |  | | . ` | |       | |    | || |  | | . ` |\___ \ 
#  | |    | |__| | |\  | |____   | |   _| || |__| | |\  |____) |
#  |_|     \____/|_| \_|\_____|  |_|  |_____\____/|_| \_|_____/ 
#                                                               
# =============================================================================
def my_text_header(my_string,
                   my_text_align='center', 
                   my_font_family='Lobster, cursive;',
                   my_font_weight=200,
                   my_font_size='36px',
                   my_line_height=1.5):
    text_header = f'<h1 style="text-align:{my_text_align}; font-family: {my_font_family}; font-weight: {my_font_weight}; font-size: {my_font_size}; line-height: {my_line_height};">{my_string}</h1>'
    st.markdown(text_header, unsafe_allow_html=True)

def my_text_paragraph(my_string,
                       my_text_align='center',
                       my_font_family='Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                       my_font_weight=200,
                       my_font_size='18px',
                       my_line_height=1.5,
                       add_border=False,
                       border_color = "#45B8AC"):
    if add_border:
        border_style = f'border: 2px solid {border_color}; border-radius: 10px; padding: 10px; box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);'
    else:
        border_style = ''
    paragraph = f'<p style="text-align:{my_text_align}; font-family:{my_font_family}; font-weight:{my_font_weight}; font-size:{my_font_size}; line-height:{my_line_height}; background-color: rgba(255, 255, 255, 0); {border_style}">{my_string}</p>'
    st.markdown(paragraph, unsafe_allow_html=True)
    
def vertical_spacer(n):
    for i in range(n):
        st.write("")
        
def show_lottie_animation(url, key, reverse=False, height=400, width=400, speed=1, loop=True, quality='high', col_sizes=[1, 3, 1], margin_before = 0, margin_after = 0):
    with open(url, "r") as file:
        animation_url = json.load(file)

    col1, col2, col3 = st.columns(col_sizes)
    with col2:
        vertical_spacer(margin_before)
        
        st_lottie(animation_url,
                  reverse=reverse,
                  height=height,
                  width=width,
                  speed=speed,
                  loop=loop,
                  quality=quality,
                  key=key
                  )
        vertical_spacer(margin_after)

def create_flipcard_gasoline(image_path_front_card=None, font_size_back='10px', my_header='', **kwargs):
    # Open the image for the front of the card
    with open(image_path_front_card, 'rb') as file:
        contents = file.read()
        data_url = base64.b64encode(contents).decode("utf-8")

    # Create empty list that will keep the HTML code needed for each card with header+text
    card_html = []

    # Append HTML code to list
    card_html.append(f"""
        <div class="flashcard">
            <div class='front'>
                <img src="data:image/png;base64,{data_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px;">
            </div>
            <div class="back">
                <h2>Instructions</h2>
                <p>
                    <br>
                    <b>Step 1:</b> Select your date range for retrieving historical U.S. gas prices*
                    <br>
                    <b>Step 2:</b> Choose a metric for assessment (Gallons/Liters).
                    <br>
                    <b>Step 3:</b> Enter your vehicle's Fuel Tank Size (Gallons).
                    <br>
                    <b>Step 4:</b> Press the <b>"Submit"</b> button from the sidebar.
                </p>
                <footer style="font-size: 14px;">
                    *Data retrieved using the API of U.S. Bureau of Labor Statistics.
                </footer>
            </div>
        </div>
    """)
    # Join all the HTML code for each card and join it into single HTML code with carousel wrapper
    carousel_html = "<div class='flipcard_stats'>" + "".join(card_html) + "</div>"
    # Display the carousel in Streamlit
    st.markdown(carousel_html, unsafe_allow_html=True)
    # Create the CSS styling for the carousel
    st.markdown(
        f"""
        <style>
        .flipcard_stats {{
          display: flex;
          justify-content: center;
          overflow-x: auto;
          scroll-snap-type: x mandatory;
          scroll-behavior: smooth;
          -webkit-overflow-scrolling: touch;
          width: 100%;
        }}
        .flashcard {{
          width: 600px;
          height: 600px;
          background-color: white;
          border-radius: 10px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
          perspective: 100px;
          margin-bottom: 10px;
          scroll-snap-align: center;
        }}
        .front, .back {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border-radius: 10px;
          backface-visibility: hidden;
          font-family: 'Ysabeau SC', sans-serif;
          text-align: center;
        }}
        .front {{
          color: white;
          transform: rotateY(0deg);
        }}
        .back {{
              color: #333333;
              background-image: linear-gradient(to bottom, #87c0b9, #88bab7, #8Badb5, #92a5b3, #909aa4);
              transform: rotateY(180deg);
              display: block;
              justify-content: flex-start;
              border: 7px solid #400c0c;
              margin: 0;
              padding: 60px;
              text-align: left;
              text-justify: inter-word;
              overflow: auto;
            }}
        .back h2 {{
          margin-bottom: 20px;
          margin-top: 0px;
        }}
        .flashcard:hover .front {{
          transform: rotateY(180deg);
        }}
        .flashcard:hover .back {{
          transform: rotateY(0deg);
        }}
        .back p {{
          margin: 10px 0;
          font-size: {font_size_back};
        }}
        footer {{
          text-align: center;
          margin-top: 20px;
          font-size: 12px;
          margin-bottom: 20px;
        }}
        </style>
        """, unsafe_allow_html=True)

def plot_gas_price(df, key=0, my_chart_color='#00008B'):
    """
    Displays a line chart of a Pandas DataFrame using Plotly Express.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to display.
    key : int or str, optional
        An optional identifier used to cache the output of the function when called with the same arguments,
        by default 0.

    Returns
    -------
    None
        The function displays the chart in the Streamlit app.

    """
    my_text_paragraph('<b>U.S. Gas Price Per Gallon</b>')
    my_text_paragraph(' Month-over-Month % Change', my_font_size='14px')

    # Create a copy of the DataFrame to avoid modifying the original data
    data_df = df.copy()

    # Create plotly line graph object
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data_df["date"], y=data_df["perct_change_value"], line=dict(color=my_chart_color, width=2, dash='solid')))

    # Customize the layout
    fig.update_layout(
        width=800,
        height=400,
        xaxis=dict(title='Date'),
        yaxis=dict(title='', tickformat='.2%'),  # Change tickformat to 'd' for integers
        legend=dict(x=0.9, y=0.9),
        plot_bgcolor='rgba(0,0,0,0)',  # Set the background to transparent
    )

    # Set labels for x and y axis
    fig.update_layout(
        title = '',
        title_x = 0.5,
        xaxis_title = "Date",
        title_font = dict(size=15),
        yaxis_title = "Month-over-Month %Δ",
        width = 800,
        height = 600,
        template = 'plotly',
        plot_bgcolor='rgba(0,0,0,0)',  # Set the background to transparent
        xaxis=dict(
            showline=True,
            showgrid=True,
            linecolor='black',
            linewidth=0.5,
            tickfont=dict(size=14, family='Arial'),
            ticks="outside",
            ticklabelmode="period",
            tickcolor="black",
            rangemode="tozero",
            gridcolor='whitesmoke'
        ),
        yaxis=dict(
            ticks="outside",
            ticklabelmode="period",
            linecolor='black',
            linewidth=0.5,
            tickcolor="black",
            rangemode="tozero",
            gridcolor='whitesmoke',
        )
    )

    # Add the range slider to the layout
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=6, label='6m', step='month', stepmode='backward'),
                    dict(count=1, label='YTD', step='year', stepmode='todate'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(step='all')
                ]),
                x=0.35,
                y=1.2,
                yanchor='auto',  # top
                font=dict(size=10),
            ),
            rangeslider=dict(  # bgcolor='45B8AC',
                visible=True,
                range=[data_df["date"].min(), data_df["date"].max()]  # Set range of slider based on data
            ),
            type='date'
        )
    )
    # Set the line color to a lighter blue and legend name
    fig.update_traces(line_color='#1E90FF', showlegend=True, name="Gas Price %Δ")

    # Set the legend position and remove legend title
    fig.update_layout(legend=dict(x=0.9, y=0.9, title=""))
    return fig

def create_gas_price_line_graph(df):
    """
    Creates a Plotly line graph object for U.S. Monthly Gas Price Per Gallon.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to plot.

    Returns
    -------
    fig : plotly.graph_objs.Figure
        The Plotly line graph object.

    """
    my_text_paragraph('<b> U.S. Gas Price Per Gallon</b>')
    my_text_paragraph(' Month-over-Month', my_font_size='14px')
    
    # Create plotly line graph object
    fig = px.line(data_frame=df, x="date", y="value")

    # Customize the layout
    fig.update_layout(
        title='',
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="Gas Price per gallon ($)",
        width=800,
        height=500,
        template='plotly',
        plot_bgcolor='rgba(0,0,0,0)',  # Set the background to transparent
        xaxis=dict(
            showline=True,
            showgrid=True,
            linecolor='black',
            linewidth=0.5,
            tickfont=dict(size=14, family='Arial'),
            ticks="outside",
            ticklabelmode="period",
            tickcolor="black",
            rangemode="tozero",
            gridcolor='whitesmoke',
            tickangle=0  # Do not rotate text 90 degrees
        ),
        yaxis=dict(
            ticks="outside",
            ticklabelmode="period",
            linecolor='black',
            linewidth=0.5,
            tickcolor="black",
            rangemode="tozero",
            gridcolor='whitesmoke',
        )
    )

    # Set the line color and legend name
    fig.update_traces(line_color='cornflowerblue', showlegend=True, name="Gas Price ($)")

    return fig

def social_media_links(margin_before = 30):
    vertical_spacer(margin_before)
    st.markdown('---')
    # Get the URL to link to
    github_url = "https://github.com/tonyhollaar/"  # Replace with your GitHub URL
    medium_url = "https://medium.com/@thollaar"  # Replace with your Medium URL
    logo_url = "https://tonyhollaar.com"  # Replace with the URL to your Website logo
    twitter_url = "https://twitter.com/tonyhollaar"  # Replace with your Twitter URL
    buymeacoffee_url = "https://www.buymeacoffee.com/tonyhollaar"  # Replace with your BuyMeACoffee URL
    
    # Generate the HTML code for the GitHub icon
    github_code = f'<a href="{github_url}"><img src="https://raw.githubusercontent.com/tonyhollaar/ForecastGenie/main/images/github-mark.png" alt="GitHub" width="32"></a>'
    
    # Generate the HTML code for the Medium icon
    medium_code = f'<a href="{medium_url}"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Medium_logo_Monogram.svg/512px-Medium_logo_Monogram.svg.png" alt="Medium" width="32"></a>'
    
    # Generate the HTML code for the logo
    logo_code = f'<a href="{logo_url}"><img src="https://raw.githubusercontent.com/tonyhollaar/ForecastGenie/main/images/logo_website.png" alt="Logo" width="32"></a>'
    
    twitter_code = f'<a href="{twitter_url}"><img src="https://raw.githubusercontent.com/tonyhollaar/ForecastGenie/main/images/twitter_logo_black.png" alt="Logo" width="32"></a>'
    
    buymeacoffee_code = f'<a href="{buymeacoffee_url}"><img src="https://raw.githubusercontent.com/tonyhollaar/ForecastGenie/main/images/buymeacoffee_logo.png" alt="buymeacoffee" height="32"></a>'
    # Render the icons using st.markdown()
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1])
    with col2:
        st.markdown(logo_code, unsafe_allow_html=True)
    with col4:
        st.markdown(medium_code, unsafe_allow_html=True)
    with col6:
        st.markdown(twitter_code, unsafe_allow_html=True)
    with col8:
        st.markdown(github_code, unsafe_allow_html=True)
    with col10:
        st.markdown(buymeacoffee_code, unsafe_allow_html=True)
        
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def update_my_metric(metric):
    if 'my_metric' not in st.session_state:
        st.session_state['my_metric'] = 'Liter'
    else:
        if metric == 'Gallons':
            st.session_state['my_metric'] = 'Liter'
        else:
            st.session_state['my_metric'] = 'Gallon'

       
def rounded_image(image_path, corner_radius):
    # Load the image as bytes
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()

    # Convert the image bytes to base64
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # Define the HTML with inline CSS for rounded corners and original fit
    html = f'''
    <div style="
        border-radius: {corner_radius}px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: center;
    ">
        <img src="data:image/png;base64,{img_base64}" style="width: 100%; height: 100%; object-fit: contain;" />
    </div>
    '''

    # Display the rounded image using st.markdown
    st.markdown(html, unsafe_allow_html=True)

def main():
    
    # Define variables
    gas_df = pd.DataFrame()
    electricity_df = pd.DataFrame()
    
    tab1, tab2, tab3 = st.tabs(['Dashboard', 'Plots', 'Raw Data'])
    with tab1:
        with st.sidebar:
            metric = None
            
            # Display logo image in sidebar
            st.image('./images/gaspricewatcher.PNG')
            
            # Display user form with options to filter data in sidebar
            with st.sidebar.form("user_form"):
                my_text_paragraph('User Settings')
                
                start_year, end_year = st.select_slider(label = "Select Year Range", options = list(range(2014, 2024)), value = (2014, 2023))  # Default range of years
                metric = st.radio(label = "Select Metric:", options = ["Gallons", "Liters"], index = 0, horizontal = False) # Default selection is "Gallons"
                
                my_metric = 'Gallon' if metric == 'Gallons' else 'Liter'
                
                if metric == 'Gallons':
                    fuel_tank_size_value = 14.00
                    fuel_per_year = 489.00
                else:
                    fuel_tank_size_value = (14*3.785411784)
                    fuel_per_year = (489.00 * 3.785411784)
                    
                gas_type = st.radio(label = "Select Type:", options = ["Regular", "Midgrade", "Premium", "Diesel"], index = 0, horizontal = False) # Default selection is "Gallons"
                fuel_tank_size = st.number_input(f'Enter the Fuel Tank Size (in {my_metric}s)', min_value = 1.0, max_value = 100.0, value = float(fuel_tank_size_value), step = 1.0)
                usage_per_year = st.number_input(label = f'Enter amount used per year (in {my_metric}s)', min_value = 1.0, value = float(fuel_per_year), step = 1.0)
                
                # electricity
                battery_capacity = st.number_input('Enter the Battery Usable Capacity (in KWH)', min_value = 1, value = 81  , step = 1)
                submit_button = st.form_submit_button(label="Submit", use_container_width = True)
            
            # Show Social Media links    
            social_media_links(margin_before = 1)
           
        # If user presses Submit button, run code
        if submit_button:
            with st.expander('', expanded = True):
                if gas_type is not 'Diesel':
                    my_text_header('Gasoline', my_font_size='54px')
                    my_text_paragraph(f'{gas_type.lower()} unleaded (in {my_metric.lower()}s)')
                elif gas_type is 'Diesel':
                    my_text_header('Diesel', my_font_size='54px')
                    my_text_paragraph(f'(in {my_metric.lower()}s)')
                    
                    
    
                # =============================================================================
                # Step 1: Create the custom BLSConnection with a connection_name
                # =============================================================================
                connection = BLSConnection("bls_connection")
    
                # =============================================================================
                # Step 2: Input parameters for the API call
                # =============================================================================
                # two timeseries are called from the API:
                # APU000074714 -> Gasoline, unleaded regular, per gallon/3.785 liters in U.S. city average, average price, not seasonally adjusted, source: https://data.bls.gov/timeseries/APU000074714
                # APU000072610 -> Electricity per KWH in U.S. city average, average price, not seasonally adjusted #source: https://beta.bls.gov/dataViewer/view/timeseries/APU000072610
                seriesids_list = ['APU000074714', 'APU000074715', 'APU000074716', 'APU000074717', 'APU000072610']
                start_year_str = str(start_year)
                end_year_str = str(end_year)
    
                # =============================================================================
                # Step 3: Fetch data using the custom connection
                # =============================================================================
                # retrieve a dictionary of dataframe(s) e.g. if multiple data id's are provided, which can be individually retrieved per dataset from https://www.bls.gov/developers/home.htm
                dataframes_dict = connection.query(seriesids_list, start_year_str, end_year_str)
    
                try:     
                    # Assign individual dataframes to named variables using tuple unpacking
                    gas_type_dict = {'regular': 'APU000074714', 'midgrade': 'APU000074715', 'premium': 'APU000074716', 'diesel': 'APU000074717'}
                    selected_key = gas_type_dict[gas_type.lower()] 
                    
                    #gas_df = dataframes_dict['APU000074714']
                    gas_df = dataframes_dict[selected_key]
                    electricity_df = dataframes_dict['APU000072610']
                except:
                    # BACKUP METHOD to retrieve saved data from .CSV file in case live connection reached maximum of e.g. 25 queries a day
                    if gas_df is None:
                        st.info('connection with API to bls.gov could not be established, backup method initiated to retrieve data from .CSV')
                        gas_df = pd.read_excel('./demo_data/gas_df.xlsx')
                        
                    if electricity_df is None:
                        electricity_df = pd.read_excel('./demo_data/electricity_df.xlsx')
                        
                    if gas_df is None or electricity_df is None:
                        st.info('connection with API to bls.gov could not be established, backup method initiated to retrieve data from .CSV')
                        
                    else:
                        st.error('Error: the dataset could not be retrieved via API nor a backup copy')
                    
                # =============================================================================
                # Step 4: preprocess gasoline dataframe (gas_df)   
                # =============================================================================
                gas_df['Price per Gallon ($)'] = gas_df['value']
                gas_df['Price per Liter ($)'] = gas_df['Price per Gallon ($)'] / 	3.785411784
                    
                # =============================================================================
                # Step 5: Display Dashboard Metrics in Streamlit
                # =============================================================================
                formatted_date = gas_df['date'].iloc[-1].strftime('%m-%d-%Y')
                my_text_paragraph(my_string = f'latest data as of {formatted_date}', my_font_size='12px')
                
                latest_value = gas_df[f'Price per {my_metric} ($)'].iloc[-1]  # Get the latest value
                delta = gas_df['perct_change_value'].iloc[-1]  # Get the delta
                
                # Show title/caption centered on page
                col1, col2, col3, col4, col5, col6, col7 = st.columns([14, 48, 1, 36, 1, 48, 12])
                with col2:
                    st.metric(label = f'Price per {my_metric}', value = f"${latest_value:.2f}", delta= f"{delta*100:.2f}%", label_visibility = 'visible',  delta_color="inverse", help = f'Gasoline, unleaded regular, per {my_metric.lower()} in U.S. city average, average price, not seasonally adjusted.')
                with col4:
                    st.metric(label = 'Full Tank', value = f"${fuel_tank_size*latest_value:.2f}",  delta= f"${delta*fuel_tank_size*latest_value:.2f}", label_visibility = 'visible',  delta_color="inverse", help = 'total cost of fuel for a full tank and month-to-month variance in usd')
                with col6:
                    # per year 489 gallons #source: https://www.api.org/news-policy-and-issues/blog/2022/05/26/top-numbers-driving-americas-gasoline-demand
                    st.metric(label = 'Estimated Yearly Cost', value = f"${usage_per_year*latest_value:.2f}",  delta= f"${delta*usage_per_year*latest_value:.2f}", label_visibility = 'visible',  delta_color="inverse", help = 'total estimated cost of fuel per year - with 489 gallons')
                
                
                # =============================================================================
                # Electricity  Metrics           
                # =============================================================================
                st.markdown('---')
                latest_value = electricity_df['value'].iloc[-1]  # Get the latest value
                delta = electricity_df['perct_change_value'].iloc[-1]  # Get the delta
                
                my_text_header('Electricity', my_font_size = '48px', my_font_family = 'Orbitron')
                my_text_paragraph('average electricity price, per kWh')
                formatted_date = electricity_df['date'].iloc[-1].strftime('%m-%d-%Y')
                my_text_paragraph(my_string = f'latest data as of {formatted_date}', my_font_size='12px')
                
                col1, col2, col3, col4, col5 = st.columns([16, 12, 1, 12, 10])
                with col2:
                    st.metric(label='Price per kWh', value = f"${latest_value:.2f}", delta= f"{delta*100:.2f}%", label_visibility = 'visible',  delta_color="inverse", help = 'Price in USD of Electricity per Kilowatt-Hour (kWh)')
                with col4:
                    st.metric(label = 'Usable Capacity Battery', value = f"${battery_capacity*latest_value:.2f}",  delta= f"${delta*battery_capacity*latest_value:.2f}", label_visibility = 'visible',  delta_color="inverse", help = 'Battery capacity in kWh')
            






            rounded_image(image_path = "./images/car_headlights.png", corner_radius = 5)
        # if user did not press submit button on dashboard tab
        else:
            # Show Cover Image
            create_flipcard_gasoline(image_path_front_card ='./images/COVER_GASOLINE.PNG', font_size_back='18px')
            
    with tab2:
        with st.expander('', expanded = True):
            # =============================================================================
            # Display the graph in Streamlit app
            # =============================================================================            
            # Absolute Values plot
            if gas_df is not None and not gas_df.empty:
                st.plotly_chart(create_gas_price_line_graph(gas_df), use_container_width = True)
            
                st.markdown('---')
                # Month over Month % Change plot
                st.plotly_chart(plot_gas_price(gas_df), use_container_width = True)

        rounded_image(image_path = './images/oldtimer.png', corner_radius = 5)
    with tab3:
        with st.expander('', expanded = True):
        
            # header
            my_text_paragraph('<b>Raw Data - Gasoline</b>')
            
            # Show animation in Streamlit 
            show_lottie_animation(url = './images/animation_lkhk7c4h.json', key = 'oil', width=160, speed = 1, col_sizes = [45,40,40])
            
            # Show Dataframe in Streamlit
            st.dataframe(gas_df, use_container_width = True)
            
            # Caption for data source
            st.caption('source: U.S. Bureau of Labor Statistics Data')
            
            # Download Button to .CSV
            csv_gas = convert_df(gas_df)
            col1, col2, col3 = st.columns([54,30,50])
            with col2: 
                st.download_button(label = "🔲 Download",
                                   data = csv_gas,
                                   file_name = 'Gas_Prices.CSV',
                                   help = 'Download your dataframe to .CSV',
                                   mime='text/csv')

            # =============================================================================
            # Electricity DF            
            # =============================================================================
            # Display the data in Streamlit
            st.markdown('---')
            
            # header
            my_text_paragraph('<b>Raw Data - Electricity</b>')
            
            # Show animation in Streamlit 
            show_lottie_animation(url = './images/animation_lkj56bhq.json', key = 'electricity', width=160, speed = 1, col_sizes = [45,40,40])
            
            # Show Dataframe in Streamlit
            st.dataframe(electricity_df, use_container_width = True)
            
            # Caption for data source
            st.caption('source: U.S. Bureau of Labor Statistics Data')
            
            # Download Button to .CSV
            csv_electricity = convert_df(electricity_df)
            col1, col2, col3 = st.columns([54,30,50])
            with col2: 
                st.download_button(label = "🔲 Download",
                                   data = csv_electricity,
                                   file_name = 'Electricity_Prices.CSV',
                                   help = 'Download your dataframe to .CSV',
                                   mime='text/csv')

    
if __name__ == "__main__":
    main()
