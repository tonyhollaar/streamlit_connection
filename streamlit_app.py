# -*- coding: utf-8 -*-
"""
                             _                        _       _               
                            (_)                      | |     | |              
   __ _  __ _ ___ _ __  _ __ _  ___ _____      ____ _| |_ ___| |__   ___ _ __ 
  / _` |/ _` / __| '_ \| '__| |/ __/ _ \ \ /\ / / _` | __/ __| '_ \ / _ \ '__|
 | (_| | (_| \__ \ |_) | |  | | (_|  __/\ V  V / (_| | || (__| | | |  __/ |   
  \__, |\__,_|___/ .__/|_|  |_|\___\___| \_/\_/ \__,_|\__\___|_| |_|\___|_|   
   __/ |         | |                                                          
  |___/          |_|                                                          

Created on Mon Jul 24 15:13:46 2023
@author: tonyhollaar
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
import streamlit as st  # Streamlit library for creating interactive web apps
import pandas as pd  # Pandas library for data manipulation and analysis
from datetime import datetime  # Datetime module for working with dates and times
from streamlit_bls_connection import BLSConnection  # Custom library for connecting to BLS API
import plotly.express as px  # Plotly Express for creating interactive visualizations
import plotly.graph_objects as go  # Plotly Graph Objects for more advanced visualizations
from streamlit_lottie import st_lottie  # Streamlit Lottie for displaying Lottie animations
import json  # JSON library for working with JSON data
import base64  # Base64 library for encoding and decoding binary data
import numpy as np  # NumPy library for numerical operations
import requests  # Requests library for making HTTP requests
from PIL import Image
            
# to convert img to html
# source: https://github.com/dataprofessor/st-demo-image-markdown/tree/master
from utilities import load_bootstrap  # Custom utility function for loading Bootstrap CSS

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
                   page_icon = "", 
                   initial_sidebar_state = "expanded") # "auto" or "expanded" or "collapsed"

# SET FONT STYLE(S)
font_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Ysabeau+SC:wght@200&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Fredericka+the+Great&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Bad+Script&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Poiret+One&display=swap');
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
                font-size: 24px;
            }
            </style>
            """, unsafe_allow_html=True)

# bootstrap icon            
search_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
</svg>
"""

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
                       link_url=None,
                       my_text_align='center',
                       my_font_family='Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                       my_font_weight=200,
                       my_font_size='18px',
                       my_line_height=1.5,
                       add_border=False,
                       border_color="#45B8AC"):
    if add_border:
        border_style = f'border: 2px solid {border_color}; border-radius: 10px; padding: 10px; box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);'
    else:
        border_style = ''
    
    if link_url:
        paragraph = f'<p style="text-align:{my_text_align}; font-family:{my_font_family}; font-weight:{my_font_weight}; font-size:{my_font_size}; line-height:{my_line_height}; background-color: rgba(255, 255, 255, 0); {border_style}">{my_string} <a href="{link_url}" target="_blank">Click here</a></p>'
    else:
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

# The function returns the Bootstrap CSS stylesheet for Streamlit.
# It loads the Bootstrap styles to improve the appearance of image
# source: https://github.com/dataprofessor/st-demo-image-markdown/blob/master/utilities.py
load_bootstrap()

def img_to_html(img_url):
    response = requests.get(img_url)
    encoded = base64.b64encode(response.content).decode()
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(encoded)
    return img_html

def create_flipcard_gasoline(image_path_front_card=None, font_size_back='10px', my_header='', **kwargs):
    # Convert the image URL to an HTML image element
    front_image_html = img_to_html(image_path_front_card)

    # Create empty list that will keep the HTML code needed for each card with header+text
    card_html = []

    # Append HTML code to list
    card_html.append(f"""
        <div class="flashcard">
            <div class='front'>
                {front_image_html}
            </div>
            <div class="back">
                <h2>Instructions</h2>
                <p>
                    <br>
                    <b>step 1:</b> Select your <b>date range</b> for retrieving historical U.S. gasoline prices*
                    <br>
                    <b>step 2:</b> Choose a <b>metric</b> for assessment i.e. <i>gallons</i> or <i>liters</i>
                    <br>
                    <b>step 3:</b> Select a <b>type of fuel</b>: <i>regular, midgrade, premium, diesel</i>
                    <br>
                    <b>step 4:</b> Enter <b>Fuel Tank Size</b> in <i>gal/L</i>
                    <br>
                    <b>step 5:</b> Enter amount of <b>fuel used per year</b> in <i>gal/L</i>
                    <br>
                    <b>step 6:</b> Enter <b>Battery Size</b> (kWh) of your Electric Vehicle (EV)</b>
                    <br>
                    <b>step 7:</b> Enter <b>Miles Per Gallon Equivalent</b> (MPGe) of your EV</b>
                    <br>
                    <b>step 8:</b> <b>[optional]</b> Enter your <b>api key</b> from BLS*
                    <br>
                    <b>step 9:</b> Press the <b>"Submit"</b> button from the sidebar
                </p>
                <footer>
                    *<b>Data Source Disclaimer</b>: data retrieved with a <i>streamlit connection</i> from the <i>U.S. bureau of labor statistics</i> API - BLS.gov cannot vouch for the data or analyses derived from these data after the data have been retrieved from BLS.gov.
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
          margin-bottom: 0px;
          margin-top: 0px;
        }}
        .flashcard:hover .front {{
          transform: rotateY(180deg);
        }}
        .flashcard:hover .back {{
          transform: rotateY(0deg);
        }}
        .back p {{
          margin: -10px 0;
          font-size: {font_size_back};
        }}
        footer {{
          text-align: left;
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

    # Create an empty Plotly figure with layout
    fig = go.Figure()

    # Check if DataFrame is None or empty
    if df is None or df.empty:
        fig.update_layout(
            width=800,
            height=400,
            xaxis=dict(title='Date'),
            yaxis=dict(title='', tickformat='.2%'),  # Change tickformat to 'd' for integers
            legend=dict(x=0.9, y=0.9),
            plot_bgcolor='rgba(0,0,0,0)',  # Set the background to transparent
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
                rangeslider=dict(
                    visible=True,
                    range=["2022-01-01", "2022-12-31"],  # Set default range for slider
                ),
                type='date'
            )
        )

    else:
        # Create a copy of the DataFrame to avoid modifying the original data
        data_df = df.copy()

        # Create plotly line graph object
        fig.add_trace(go.Scatter(x=data_df["date"], y=data_df["%_change_value"], line=dict(color=my_chart_color, width=2, dash='solid')))

        # Customize the layout for non-empty DataFrame
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
            title='',
            title_x=0.5,
            xaxis_title="Date",
            title_font=dict(size=15),
            yaxis_title="Month-over-Month %Δ",
            width=800,
            height=600,
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
                rangeslider=dict(
                    visible=True,
                    range=[data_df["date"].min(), data_df["date"].max()],  # Set range of slider based on data
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
    # Create an empty plotly line graph object if the DataFrame is empty or None
    if df is None or df.empty:
        my_text_paragraph('<b> U.S. Gas Price Per Gallon</b>')
        my_text_paragraph(' Month-over-Month', my_font_size='14px')
        
        fig = go.Figure()
    else:
        my_text_paragraph('<b> U.S. Gas Price Per Gallon</b>')
        my_text_paragraph(' Month-over-Month', my_font_size='14px')
        
        # Create plotly line graph object
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df["value"], mode="lines", line_color='cornflowerblue', name="Gas Price ($)"))

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

    return fig

def my_bubbles(my_string, my_background_color="#2CB8A1"):
    gradient = f"-webkit-linear-gradient(45deg, {my_background_color}, #2CB8A1, #0072B2)"
    text_style = f"text-align: center; font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif; font-weight: 200; font-size: 36px; line-height: 1.5; -webkit-background-clip: text; -webkit-text-fill-color: black; padding: 20px; position: relative;"
    st.markdown(f'''
        <div style="position: relative;">
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; z-index: -1; opacity: 0.2;"></div>
            <h1 style="{text_style}">
                <center>{my_string}</center>
                <div style="position: absolute; top: -30px; left: 80px;">
                    <div style="background-color: #0072B2; width: 8px; height: 8px; border-radius: 50%; animation: bubble 7s infinite;"></div>
                </div>
                <div style="position: absolute; top: -20px; right: 100px;">
                    <div style="background-color: #FF0000; width: 14px; height: 14px; border-radius: 50%; animation: bubble 4s infinite;"></div>
                </div>
                <div style="position: absolute; top: 10px; right: 50px;">
                    <div style="background-color: #0072B2; width: 8px; height: 8px; border-radius: 50%; animation: bubble 5s infinite;"></div>
                </div>
                <div style="position: absolute; top: -20px; left: 60px;">
                    <div style="background-color: #88466D; width: 8px; height: 8px; border-radius: 50%; animation: bubble 6s infinite;"></div>
                </div>
                <div style="position: absolute; top: 0px; left: -10px;">
                    <div style="background-color: #2CB8A1; width: 12px; height: 12px; border-radius: 50%; animation: bubble 7s infinite;"></div>
                </div>
                <div style="position: absolute; top: 10px; right: -20px;">
                    <div style="background-color: #7B52AB; width: 10px; height: 10px; border-radius: 50%; animation: bubble 10s infinite;"></div>
                </div>
                <div style="position: absolute; top: -20px; left: 150px;">
                    <div style="background-color: #FF9F00; width: 8px; height: 8px; border-radius: 50%; animation: bubble 20s infinite;"></div>
                </div>
                <div style="position: absolute; top: 25px; right: 170px;">
                    <div style="background-color: #FF6F61; width: 12px; height: 12px; border-radius: 50%; animation: bubble 4s infinite;"></div>
                </div>
                <div style="position: absolute; top: -30px; right: 120px;">
                <div style="background-color: #440154; width: 10px; height: 10px; border-radius: 50%; animation: bubble 5s infinite;"></div>
                </div>
                <div style="position: absolute; top: -20px; left: 150px;">
                <div style="background-color: #2CB8A1; width: 8px; height: 8px; border-radius: 50%; animation: bubble 6s infinite;"></div>
                </div>
                <div style="position: absolute; top: -10px; right: 20px;">
                <div style="background-color: #FFC300; width: 12px; height: 12px; border-radius: 50%; animation: bubble 7s infinite;"></div>
                </div>
                </h1>
                <style>
                @keyframes bubble {{
                0% {{
                transform: translateY(0);
                }}
                50% {{
                transform: translateY(+50px);
                }}
                100% {{
                transform: translateY(0);
                }}
                }}
                .bubble-container div {{
                margin: 10px;
                }}
                </style>
                </div>
                ''', unsafe_allow_html=True)

def social_media_links(margin_before = 0):
    vertical_spacer(margin_before)
    
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
    # =============================================================================
    # Initialize variables
    # =============================================================================
    gas_df = pd.DataFrame() # to save gasoline prices
    electricity_df = pd.DataFrame() # to save electricity prices
    metric = None # Imperial System / Metric System
    latest_value_gas = None #initialize variable for holding latest gasoline price value in USD
                
    # Define user tabs in Streamlit
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['🛡️ Dashboard', '📈 Plots', '🔢 Raw Data', '🛣️ Route66', 'ℹ️ Streamlit Connection API', '📜 Disclaimer'])
    with tab1:
        with st.sidebar:

            gaspricewatcher_logo = Image.open('./images/gaspricewatcher.png')
            st.image(gaspricewatcher_logo) #display logo
            
            # =============================================================================
            #             # Display user form with options to filter data in sidebar
            # =============================================================================
            with st.sidebar.form("user_form"):
                my_text_paragraph('User Settings')
                start_year, end_year = st.select_slider(label = "📆 Select Date Range", 
                                                        options = list(range(2014, 2024)), 
                                                        value = (2014, 2023))  # Default range of years
                
                metric = st.radio(label = "📐 Select System of Measurement", 
                                  options = ["Imperial System", "Metric System"], 
                                  index = 0, 
                                  horizontal = True, 
                                  help="""If you select the **Imperial System**, the units of measurement will be in `gallons` for fuel and `miles` for distance (used in the U.S.).
                                        Alternatively, if you choose the **Metric System**, the units of measurement will be in `liters` for fuel and `kilometers` for distance (used by most of the world).""")
                
                fuel_efficiency_metric = "miles per gallon" if metric == "Imperial System" else "kilometers per liter"
                fuel_efficiency_metric_abbrev = "(MPG)" if metric == "Imperial System" else "(KM/L)"
                distance_metric = "miles" if metric == "Imperial System" else "km"
                my_metric = 'Gallon' if metric == 'Imperial System' else 'Liter'
                fuel_tank_size_value = 14.00 if metric == 'Imperial System' else 14 * 3.785411784
                fuel_per_year = 489.00 if metric == 'Imperial System' else 489.00 * 3.785411784
                
                # miles to km = 1.60934, average miles per gallon = 25.40 (user can adjust), 3.78541 liters per gallon
                fuel_efficiency_value = 25.40 if metric == 'Imperial System' else 25.40 * (1.60934 / 3.785411784)
                
                gas_type = st.radio(label = "⛽ Select Fuel Type", 
                                    options = ["Regular", "Midgrade", "Premium", "Diesel"], 
                                    index = 0, # Default selection is "Gallons"
                                    horizontal = True) 
                
                fuel_tank_size = st.number_input(f'🕳️ Enter the Fuel Tank Size :green[(in {my_metric}s)]', 
                                                 min_value = 1.0, 
                                                 max_value = 100.0, 
                                                 value = float(fuel_tank_size_value), 
                                                 step = 1.0)
                
                usage_per_year = st.number_input(label = f'🛢️ Enter the fuel amount used per year :green[(in {my_metric}s)]', 
                                                 min_value = 1.0, 
                                                 value = float(fuel_per_year), 
                                                 step = 1.0)
                
                fuel_efficiency = st.number_input(label = f'🚗 Enter the fuel efficiency in {fuel_efficiency_metric} :green[{fuel_efficiency_metric_abbrev}]', 
                                                  min_value = 1.0, 
                                                  value = fuel_efficiency_value, 
                                                  step = 1.0)
                st.markdown('---')
                battery_capacity = st.number_input(label = '🔋 Enter the Battery Usable Capacity :green[(in KWH)]', 
                                                   min_value = 1, 
                                                   value = 81, 
                                                   step = 1)
                miles_per_gallon_equivalent = st.number_input(label = '🚙 Enter the MPGe of your electric vehicle (EV)', 
                                                              min_value = 1, 
                                                              value = 97, 
                                                              step = 1, 
                                                              help = '''MPGe stands for `miles per gallon of gasoline-equivalent`. This is a measurement of an EV's fuel efficiency.''')
                st.markdown('---')
                api_key_input = st.text_input("🔑 **[OPTIONAL]** Enter API Key :green[(U.S. Bureau of Labor Statistics)]", 
                                              value = '', 
                                              help = '''This is :green[**not required**] to retrieve data! 
                                                        However, with an API key you can:  
                                                        - execute up to 500 **queries** per day versus 25 **queries** per day  
                                                        - obtain additional **metadata** such as: *series_title*, *survey_name*, *catalog*  
                                                        To obtain an API Key, register at https://data.bls.gov/registrationEngine/''')
                                                        
                submit_button = st.form_submit_button(label="Submit", use_container_width = True)
            
            social_media_links(margin_before = 0) #Show Social Media links    
           
        # If user presses Submit button, run code
        if submit_button:
            st.toast('😇 Please wait while I pick-up your data!')
            
            with st.expander('', expanded = True):
                if gas_type != 'Diesel':
                    my_text_header('Gasoline', my_font_size='54px')
                    my_text_paragraph(f'{gas_type.lower()} unleaded in {my_metric.lower()}s')
                elif gas_type == 'Diesel':
                    my_text_header('Diesel', my_font_size='54px')
                    my_text_paragraph(f'in {my_metric.lower()}s')
                    
                # =============================================================================
                # Step 1: Create Connection object with U.S. Bureau of Labor Statistics API
                # =============================================================================
                conn = st.connection('bls', type=BLSConnection)
    
                # =============================================================================
                # Step 2: Input parameters for the API call
                # =============================================================================
                # 5 different timeseries are called from the API:
                # - APU000074714 -> Gasoline, unleaded regular, per gallon/3.785 liters in U.S. city average, average price, not seasonally adjusted, source: https://data.bls.gov/timeseries/APU000074714
                # - APU000074715 -> Gasoline, unleaded midgrade, per gallon/3.785 liters in U.S. city average, average price, not seasonally adjusted
                # - APU000074716 -> Gasoline, unleaded premium, per gallon/3.785 liters in U.S. city average, average price, not seasonally adjusted
                # - APU000072610 -> Automotive diesel fuel, per gallon/3.785 liters in U.S. city average, average price, not seasonally adjusted
                # - APU000072610 -> Electricity per KWH in U.S. city average, average price, not seasonally adjusted #source: https://beta.bls.gov/dataViewer/view/timeseries/APU000072610
                seriesids_list = ['APU000074714', 'APU000074715', 'APU000074716', 'APU000074717', 'APU000072610']
                start_year_str = str(start_year)
                end_year_str = str(end_year)
    
                # =============================================================================
                # Step 3: Fetch data using the custom connection
                # =============================================================================
               
                # =============================================================================
                # [OPTIONAL] Retrieve the API key from Streamlit secrets -> not needed but higher amount of daily queries allowed e.g. 500 versus 25                
                # register at https://data.bls.gov/registrationEngine/ to obtain your API key and put it in .streamlit/secrets.toml file
                # [connections_bls]
                # api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                # =============================================================================
                try:
                    # Get the API key from Streamlit secrets
                    api_key_secrets = st.secrets["connections_bls"]["api_key"]
                except:
                    api_key_secrets = None
                
                # Check if the user has provided an API key through the form
                if api_key_input:
                    api_key = api_key_input
                    st.toast('Your API Key was used from the sidebar!', icon='😍')
                elif api_key_secrets:
                    api_key = api_key_secrets
                    st.toast('Your API Key was found in secrets.toml file!', icon='😍')
                else:
                    api_key = None
                    st.toast('No API Key was provided, no worries!', icon='😇')
                
                # Retrieve a dictionary of dataframe(s) e.g. if multiple data id's are provided
                # which can be individually retrieved per dataset from https://www.bls.gov/developers/home.htm
                dataframes_dict = conn.query(seriesids_list, start_year_str, end_year_str, api_key=api_key, catalog=True, calculations=True, annualaverage=True, aspects=True)
                #dataframes_dict = conn.query(seriesids_list, start_year_str, end_year_str, api_key=None) # TEST
    
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
                        st.error('Error: the dataset could not be retrieved via API nor a backup copy.')
                    
                # =============================================================================
                # Step 4: preprocess gasoline dataframe (gas_df)   
                # =============================================================================
                gas_df['Price per Gallon ($)'] = gas_df['value']
                gas_df['Price per Liter ($)'] = gas_df['Price per Gallon ($)'] / 	3.785411784
                    
                # =============================================================================
                # Step 5: Display Dashboard Metrics in Streamlit
                # =============================================================================
                formatted_date = gas_df['date'].iloc[-1].strftime('%m-%d-%Y')
                my_text_paragraph(my_string = f'latest data as of {formatted_date} (mm/dd/yyyy)', my_font_size='12px')
                

                latest_value_gas = gas_df[f'Price per {my_metric} ($)'].iloc[-1]  # Get the latest value
                delta_gas = gas_df['%_change_value'].iloc[-1]                 # Get the delta
                
                col1, col2, col3, col4, col5, col6, col7 = st.columns([14, 48, 1, 36, 1, 48, 12])
                with col2:
                    fuel_type_text = f'Gasoline, **unleaded {gas_type.lower()}**' if gas_type != 'Diesel' else f'Diesel'
                    st.metric(label = f'Price per {my_metric}', value = f"${latest_value_gas:.2f}", delta= f"{delta_gas*100:.2f}%", delta_color="inverse", help = f'''**{fuel_type_text}**, per **{my_metric.lower()}** in U.S. city average, average price, not seasonally adjusted.  Below it, you can find the **month-to-month variance** as a percentage change, relative to the previous month's price per gallon.''')
                with col4:
                    st.metric(label = 'Full Tank', value = f"${fuel_tank_size*latest_value_gas:.2f}",  delta= f"${delta_gas*fuel_tank_size*latest_value_gas:.2f}", delta_color="inverse", help = 'total cost of fuel for a full tank and month-to-month variance in usd.')
                with col6:
                    # per year 489 gallons #source: https://www.api.org/news-policy-and-issues/blog/2022/05/26/top-numbers-driving-americas-gasoline-demand
                    yearly_cost_gas = usage_per_year * latest_value_gas
                    st.metric(label = 'Estimated Yearly Cost', value = f"${yearly_cost_gas:.2f}",  delta= f"${delta_gas*usage_per_year*latest_value_gas:.2f}", label_visibility = 'visible', delta_color="inverse", help = f'The total estimated yearly cost is calculated based on a consumption of {int(usage_per_year)} {my_metric.lower()}s, with the month-to-month variance shown in USD below.')

                col1, col2, col3, col4, col5, col6, col7 = st.columns([14, 48, 1, 36, 1, 48, 12])
                with col2:
                    st.metric(label = f'{fuel_efficiency_metric}', value = f"{fuel_efficiency:,.2f}")
                with col4:
                    # Calculate miles (or kilometers) traveled
                    distance_traveled = fuel_efficiency * fuel_tank_size
                    st.metric(label = f'Range in {distance_metric}', value = f"{distance_traveled:,.0f}", help = f'Estimated distance in {distance_metric} that can be traveled with a full tank.')
                with col6:
                    yearly_distance_traveled = fuel_efficiency * usage_per_year
                    st.metric(label = f'Yearly distance in {distance_metric}', value = f"{yearly_distance_traveled:,.0f}", help = f'''Estimated **yearly distance** in {distance_metric} that can be traveled. **formula:** `{fuel_efficiency} * {usage_per_year}` rounded to nearest whole number.''')

                # =============================================================================
                # Electricity  Metrics           
                # =============================================================================
                st.markdown('---')
                latest_value_electricity = electricity_df['value'].iloc[-1]  # Get the latest value
                delta_electricity = electricity_df['%_change_value'].iloc[-1]  # Get the delta
                
                my_text_header('Electricity', my_font_size = '48px', my_font_family = 'Orbitron')
                my_text_paragraph('average electricity price, per kWh')
                formatted_date = electricity_df['date'].iloc[-1].strftime('%m-%d-%Y')
                my_text_paragraph(my_string = f'latest data as of {formatted_date} (mm/dd/yyyy)', my_font_size='12px')
                
                # convert to km if metric system is selected by user else miles
                distance_traveled_electric = (battery_capacity * miles_per_gallon_equivalent / 33.7)  if metric == 'Imperial System' else 1.60934*(battery_capacity * miles_per_gallon_equivalent / 33.7)
                
                col1, col2, col3, col4, col5, col6, col7 = st.columns([14, 48, 1, 36, 1, 48, 12])
                with col2:
                    st.metric(label='Price per kWh', value = f"${latest_value_electricity:.2f}", delta= f"{delta_electricity*100:.2f}%", label_visibility = 'visible',  delta_color="inverse", help = 'Price in USD of Electricity per Kilowatt-Hour (kWh)')
                with col4:
                    st.metric(label = 'Full Battery', value = f"${battery_capacity*latest_value_electricity:.2f}",  delta= f"${delta_electricity*battery_capacity*latest_value_electricity:.2f}", label_visibility = 'visible',  delta_color="inverse", help = 'Usable Battery capacity in kWh')
                with col6:
                    # per year 489 gallons #source: https://www.api.org/news-policy-and-issues/blog/2022/05/26/top-numbers-driving-americas-gasoline-demand
                    yearly_cost_electricity = (yearly_distance_traveled/distance_traveled_electric)*(battery_capacity*latest_value_electricity)
                    st.metric(label = 'Estimated Yearly Cost', value = f"${yearly_cost_electricity:.2f}", delta = f"${delta_electricity*(yearly_distance_traveled/distance_traveled_electric)*(battery_capacity*latest_value_electricity):.2f}", label_visibility = 'visible', delta_color="inverse", help = f'The total estimated yearly cost is calculated based on a consumption of {int(usage_per_year)} {my_metric.lower()}s, with the month-to-month variance shown in USD below.')
                
                col1, col2, col3, col4, col5, col6, col7 = st.columns([14, 48, 1, 36, 1, 48, 12])
                with col2:
                    #  one gallon of gas contains the equivalent to 33.7 kWh of electrical power
                    st.metric(label = f'MPGe', value = f"{miles_per_gallon_equivalent:,.2f}", help = '''miles per gallon of gasoline-equivalent''')
                with col4:
                    # distance = (battery capacity in kWh) x (MPGe) / 33.7
                    
                    st.metric(label = f'Range in {distance_metric}', value = f"{distance_traveled_electric:,.0f}", 
                              help = f'Estimated distance in {distance_metric} that can be traveled with a full battery charge.\n\nThe formula used for calculation is: distance_traveled_electric = battery_capacity * miles_per_kWh / 33.7.\n\nMiles per kWh (m/kWh) is a measure of how efficient the electric vehicle is in terms of energy consumption. It indicates the number of miles the vehicle can travel on one kilowatt-hour of electricity. The higher the miles per kWh value, the more efficient the vehicle.\n\nThe constant 33.7 is used to convert the miles per kWh value to miles per gallon equivalent (MPGe) for comparison with traditional gasoline-powered vehicles. It represents the energy content of one gallon of gasoline in kilowatt-hours.\n\nPlease note that the actual distance traveled may vary depending on driving conditions, vehicle model, and battery health.')
                with col6:
                    yearly_distance_traveled = fuel_efficiency * usage_per_year
                    st.metric(label = f'Yearly distance in {distance_metric}', value = f"{yearly_distance_traveled:,.0f}", help = f'''set equal to yearly distance in miles of gasoline car for comparison of yearly cost''')
                
                # =============================================================================
                # Comparison / Differences                    
                # =============================================================================
                st.markdown('---')
                my_text_header('Comparison', my_font_size = '56px', my_font_family = 'Permanent Marker')
                my_text_paragraph('<b>gasoline vs. electricity</b>', my_font_size = '18px', my_font_family = 'Ysabeau SC')
                
                col1, col2, col3, col4, col5 = st.columns([2,4,1,4,1])
                with col2:
                    # =============================================================================
                    # Cost per 100 miles/km
                    # =============================================================================
                    # GAS
                    # Step 1: Calculate the number of gallons needed to cover 100 (miles).
                    num_gallons_100 = 100 / fuel_efficiency
                    
                    # Step 2: Calculate the cost of the required gallons.
                    cost_100_distance_metric = latest_value_gas * num_gallons_100
                    
                    # ELECTRIC
                    cost_ev_100_distance_metric = (100 / miles_per_gallon_equivalent) * (33.7 * latest_value_electricity) if metric == 'Imperial System' else (160.934 / miles_per_gallon_equivalent) * (10.53125 * latest_value_electricity)

                    # Diff
                    delta_gas_ev_100 = (cost_ev_100_distance_metric - cost_100_distance_metric)/cost_100_distance_metric
                    
                    fuel_efficiency_metric_abbrev_nobrackets = 'MPGe'  if metric == 'Imperial System' else 'KM/L equivalent'
                    
                    # 8.90259816447 kWh is 1 liter equivalent in kwh
                    # 33.7 kWh is 1 gallon equivalent in kwh
                    kwh_to_metric = '33.7' if metric == 'Imperial System' else '8.9'
                    
                    st.metric(label = f'Cost per 100 {distance_metric}', 
                              value = f"${cost_100_distance_metric:.2f} vs. ${cost_ev_100_distance_metric:.2f}", 
                              delta = f"{delta_gas_ev_100:.2%}",  delta_color="inverse", 
                              help = f'''comparison of the `cost per 100 {distance_metric}` in USD.   
                                      formula for fuel-powered vehicle:  
                                      - $Cost\ per\ 100\ {distance_metric} = \\dfrac{{100}}{{\\text{{Vehicle's {fuel_efficiency_metric_abbrev_nobrackets}}}}} \\times \\text{{Price per {my_metric}}}$  
                                      formula for electric vehicle:  
                                      - $Cost\ per\ 100\ {distance_metric} = \\dfrac{{100}}{{\\text{{Vehicle's {fuel_efficiency_metric_abbrev_nobrackets}}}}} \\times (\\text{{Price per kWh}} \\times {kwh_to_metric} \\text{{ kWh}})$ 
                                      ''')
                    # =============================================================================
                    # Range in miles/km                 
                    # =============================================================================
                    delta_range =  (distance_traveled_electric - distance_traveled) / distance_traveled
                    st.metric(label = f'range in {distance_metric}', 
                              value = f"{distance_traveled:.0f} vs. {distance_traveled_electric:.0f}", 
                              delta = f"{delta_range:.2%}", 
                              help = f'''comparison of the `maximum estimated distance`, in **{distance_metric}**, that a vehicle can travel on a **full gasoline tank** versus an electric vehicle on a **full battery charge**, before needing a refuel or recharge.''')

                with col4:
                    # =============================================================================
                    # Yearly Cost                    
                    # =============================================================================
                    yearly_savings = (yearly_cost_electricity - yearly_cost_gas)
                    savings_str = f"${yearly_savings:,.2f}" if yearly_savings >= 0 else f"-${abs(yearly_savings):,.2f}"
                    st.metric(
                        label='Estimated Yearly Cost',
                        value=f"${yearly_cost_gas:,.0f} vs. ${yearly_cost_electricity:,.0f}",
                        delta=savings_str,
                        delta_color='inverse',
                        help='''comparison of estimated `yearly cost` in USD.  
                        Formula for fuel-powered vehicle:  
                        - $Estimated\\ Yearly\\ Cost = \\text{{Fuel Amount in Gallons used Per Year}} \\times  \\text{{Price per gallon}}$  
                        Formula for electric vehicle:  
                        - $Range\ Battery\ = \\left( \\dfrac{{\\text{{battery\ capacity (kWh)}} \\times \\text{{MPGe}}}}{{33.7 \\text{{ kWh}}}} \\right)$  
                        - $Estimated\\ Yearly\\ Cost = \\dfrac{{\\text{{yearly distance traveled}}}}{{\\text{{range battery}}}} \\times (\\text{{battery capacity (kWh)}} \\times \\text{{Price per kWh}})$  
                        ''')
                    
                    # =============================================================================
                    # 5 Year Cost                    
                    # =============================================================================
                    five_year_savings_str = f"${yearly_savings*5:,.2f}" if yearly_savings >= 0 else f"-${abs(yearly_savings*5):,.2f}"
                    st.metric(label = 'Estimated 5 Year Cost', 
                              value = f"${yearly_cost_gas*5:,.0f} vs. ${yearly_cost_electricity*5:,.0f}", 
                              delta = five_year_savings_str, 
                              delta_color = 'inverse',
                              help = '''comparison of estimated `5 year cost` in USD.  
                              Formula:    
                              - $5\\ Year\\ Cost = Yearly\\ Cost \\times \\text{{5}}$
                                     ''')
                
                col1, col2 = st.columns([1,20])
                with col2:
                    vertical_spacer(2)
                    message = st.chat_message("assistant", avatar = "ℹ️")
                    message.write("the arrows indicate estimated savings/costs if you switch to an EV.")
                    
            rounded_image(image_path = "./images/car_headlights.png", corner_radius = 5) #round image corners
        
        # if user did not press submit button on dashboard tab
        else:
            image_url = 'https://raw.githubusercontent.com/tonyhollaar/streamlit_connection/main/images/COVER_GASOLINE.png'
            create_flipcard_gasoline(image_path_front_card = image_url,
                                     #image_path_front_card ='./images/cover_gasoline.png', 
                                     font_size_back='16px') #Show Cover Image
    
    # PLOTS TAB
    with tab2:
        with st.expander('', expanded = True):
            my_text_header('Plots', my_font_size='48px', my_font_family='Fredericka the Great')
            # =============================================================================
            # Display the graph in Streamlit app
            # =============================================================================            
            # Absolute Values plot
            st.plotly_chart(create_gas_price_line_graph(gas_df), 
                            use_container_width = True)
            st.markdown('---')
            
            # Month over Month % Change plot
            st.plotly_chart(plot_gas_price(gas_df), 
                            use_container_width = True)

        rounded_image(image_path = './images/oldtimer.png', 
                      corner_radius = 5) #round image corners
    # RAW DATA TAB
    with tab3:
        with st.expander('', expanded = True):
            # set header
            my_text_header('Raw Data', my_font_size='48px', my_font_family='Bad Script')
            
            # Set subheader on page in Streamlit
            if gas_type != 'Diesel':
                my_text_paragraph('<b>Gasoline</b>')
                my_text_paragraph(f'{gas_type.lower()}')
            elif gas_type == 'Diesel':
                my_text_paragraph('<b>Diesel</b>')
            
            # Show lottie animation in Streamlit 
            show_lottie_animation(url = './images/animation_lkhk7c4h.json', key = 'oil', width=160, speed = 1, col_sizes = [45,40,40])
            
            # Show Dataframe in Streamlit
            st.dataframe(gas_df, use_container_width = True)
            
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
            
            # set header
            #my_text_header('Raw Data', my_font_size='48px', my_font_family='Bad Script')
            vertical_spacer(2)
            
            # set subheader
            my_text_paragraph('<b>Electricity</b>')
            
            # Show animation in Streamlit 
            show_lottie_animation(url = './images/animation_lkj56bhq.json', key = 'electricity', width=160, speed = 1, col_sizes = [45,40,40])
            
            # Show Dataframe in Streamlit
            st.dataframe(electricity_df, use_container_width = True)
            
            # Download Button to .CSV
            csv_electricity = convert_df(electricity_df)
            col1, col2, col3 = st.columns([54,30,50])
            with col2: 
                st.download_button(label = "🔲 Download",
                                   data = csv_electricity,
                                   file_name = 'Electricity_Prices.CSV',
                                   help = 'Download your dataframe to .CSV',
                                   mime='text/csv')
    # ROUTE66 TAB
    with tab4:
        with st.expander('', expanded = True):
            my_text_header('ROUTE 66', my_font_size = '48px', my_font_family = 'Archivo Black')
            
            # check if data is present then calculate total cost one way trip of route 66 e.g. (2278 miles / fuel efficiency) * latest retrieved price per gallon
            if latest_value_gas is not None:
                cost_route66 = round(2278/fuel_efficiency*latest_value_gas, 2) if metric == 'Imperial System' else round(2278 * 1.60934/fuel_efficiency*latest_value_gas, 2)
            else:
                cost_route66 = ' - '
                
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 6, 1, 6, 1, 6, 1])
            with col2:
                distance_route66 = 2278 if metric == 'Imperial System' else 2278 * 1.60934
                st.metric(label = f'Distance (in {distance_metric})', value = f"{distance_route66:,.0f}")
            with col4:
                st.metric(label = f'Fuel Efficiency {fuel_efficiency_metric_abbrev}', value = f"{fuel_efficiency:,.2f}", help = f'Fuel Efficiency in {fuel_efficiency_metric}')
            with col6:
                st.metric(label = 'Cost one-way trip', value = f"${cost_route66}", help = f'**Estimated cost** for **one-way trip** with fuel-powered vehicle based on **price per {my_metric.lower()}** in USD.')
            
            # Define the locations and their coordinates along with random population sizes
            locations = {
                "Chicago": (41.8781, -87.6298),
                "Dwight": (41.1036, -88.4252),
                "Pontiac": (40.8806, -88.6298),
                "Springfield IL": (39.7817, -89.6501),
                "Staunton": (39.0128, -89.7928),
                "St. Louis": (38.6270, -90.1994),
                "Cuba": (38.0623, -91.4032),
                "Rolla": (37.9514, -91.7713),
                "Lebanon": (37.6805, -92.6633),
                "Springfield MO": (37.2086, -93.2923),
                "Joplin": (37.0842, -94.5133),
                "Galena": (37.0758, -94.6413),
                "Tulsa": (36.1539, -95.9925),
                "Oklahoma City": (35.4676, -97.5164),
                "Elk City": (35.4058, -99.4043),
                "Shamrock": (35.2219, -101.8313),
                "Amarillo": (35.2219, -101.8313),
                "Glenrio": (35.0417, -103.9533),
                "Tucumcari": (35.1717, -103.7246),
                "Santa Rosa": (34.9381, -104.6774),
                "Santa Fe": (35.6869, -105.9378),
                "Albuquerque": (35.0844, -106.6504),
                "Grants": (35.1478, -107.8514),
                "Gallup": (35.5281, -108.7426),
                "Holbrook": (34.9022, -110.1598),
                "Winslow": (35.0242, -110.6974),
                "Flagstaff": (35.1983, -111.6513),
                "Seligman": (35.3258, -112.8766),
                "Kingman": (35.1894, -114.0530),
                "Oatman": (35.0264, -114.3834),
                "Amboy": (34.5531, -115.7500),
                "Barstow": (34.8958, -117.0173),
                "Santa Monica Pier, California": (34.0101, -118.4961)
            }
        
            # Random population sizes for demonstration purposes
            population_sizes = {
                "Chicago": 2720546,
                "Dwight": 4070,
                "Pontiac": 5855,
                "Springfield IL": 115715,
                "Staunton": 5008,
                "St. Louis": 3028385,
                "Cuba": 3363,
                "Rolla": 20301,
                "Lebanon": 14296,
                "Springfield MO": 167882,
                "Joplin": 50821,
                "Galena": 3113,
                "Tulsa": 651880,
                "Oklahoma City": 655057,
                "Elk City": 11970,
                "Shamrock": 1833,
                "Amarillo": 199371,
                "Glenrio": 30,
                "Tucumcari": 4655,
                "Santa Rosa": 5587,
                "Santa Fe": 84683,
                "Albuquerque": 564036,
                "Grants": 9142,
                "Gallup": 21404,
                "Holbrook": 5232,
                "Winslow": 9737,
                "Flagstaff": 77436,
                "Seligman": 456,
                "Kingman": 29773,
                "Oatman": 27,
                "Amboy": 10,
                "Barstow": 23878,
                "Santa Monica Pier, California": 80274
            }
            
            # Create a Pandas DataFrame from the locations dictionary
            df = pd.DataFrame(locations.values(), columns=["latitude", "longitude"], index=locations.keys())
        
            # Add population size and normalize it for size variation
            df["population"] = [population_sizes[loc] for loc in df.index]
        
            # Use pandas qcut to create relative population size bins
            df["population_bin"] = pd.qcut(df["population"], 10, labels=False)
            
            # Calculate the marker size based on the bin (size increases with bin number)
            df["size"] = 20 + 30 * df["population_bin"] * 200 #multiplied by scaling factor to make it visually appealing in map plot
                    
            # Generate random RGBA colors for each location with 50% transparency
            colors = [(np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256), 0.5) for _ in range(len(df))]
        
            # Add colors to the DataFrame
            df["color"] = colors
        
            # Display the map using st.map with size and color
            st.map(df, latitude='latitude', longitude='longitude', size='size', color='color', zoom=3)
            st.dataframe(df, use_container_width = True)
            st.image('./images/route66_logo.png')
            st.caption('''Disclaimer: This app provides information about selected locations along Route 66 but does not cover all places. It is intended for general informational purposes only and does not serve as a comprehensive travel guide. Users are encouraged to verify details and consult official travel resources for a complete representation of locations along Route 66. The app's creator makes no warranties about the accuracy or reliability of the content and shall not be held liable for any damages or losses arising from its use. Use this app responsibly and enjoy your journey along Route 66!''')
    
    # ABOUT TAB
    with tab5:
        with st.expander('', expanded = True):
            my_bubbles(my_string = '')
            my_text_header('Streamlit Connection API', my_font_size = '48px', my_font_family = 'Pacifico')
                        
            col1, col2, col3 = st.columns([1, 10, 1])
            with col2:
                vertical_spacer(2)
                my_text_paragraph(f'''This application is created as part of the <b><span style="color: #FF4E61;"> Streamlit Connections Hackathon 🎉</span></b> <a href="https://discuss.streamlit.io/t/connections-hackathon/47574" target="_blank">contest</a>. 
                                  The <i>goal</i> of this app is to demonstrate how to easily setup and retrieve data with a Streamlit connection from <b>APIs</b> (Application Programming Interfaces) and create amazing applications!
                                  This app retrieves data from the API from the <i>U.S. Bureau of Labor Statistics </i> (BLS) by utilizing a custom built <b><span style="color: #FF4E61;"> Streamlit </span></b> connection 🔌 and being able to query {search_icon} the dataset(s) and save them as <a href="https://pandas.pydata.org/" target="_blank">pandas</a> dataframe(s). This is a more user-friendly approach versus original Python code from BLS, 
                                  found at <a href="https://www.bls.gov/developers/api_python.htm#python2" target="_blank">www.bls.gov</a>. Note that <a href="https://www.bls.gov/developers/termsOfService.htm" target="_blank">Terms of Service</a> apply e.g. BLS.gov cannot vouch for the data or analyses derived from these data after the data have been retrieved from BLS.gov.
                                  <br>
                                  For more information about the <b><span style="color: #6f59f3;">streamlit_bls_connection</span></b> Python package, please refer to the official <a href="https://pypi.org/project/streamlit-bls-connection/" target=_blank">documentation</a>.
                                  Check out below example to get started if you would like to use it👇!
                                  ''', my_text_align = 'justify')
                vertical_spacer(1)
                st.image('./images/socket.png')
                vertical_spacer(1)
                my_text_paragraph('<b><span style="color: #6f59f3;">example</span></b>', my_font_family = 'Ysabeau SC', add_border=True, my_font_weight=600, my_font_size='22px', border_color = "#6f59f3")
                
                # Show codeblock in Streamlit
                my_text_paragraph('''''')
                st.code('''
                        # Step 0: install the package
                        pip install streamlit_bls_connection
                        ''', language='python')
                
                # define codeblock
                code = '''
                        import streamlit as st
                        from streamlit_bls_connection import BLSConnection
                                    
                        # Step 1: Setup connection to US Bureau of Labor Statistics
                        conn = st.experimental_connection('bls', type=BLSConnection)
                        
                        # Step 2: Define input parameters
                        # Tip: one or multiple Series ID's* can be retrieved
                        seriesids_list = ['APU000074714', 'APU000072610']
                        start_year_str = '2014' # start of date range
                        end_year_str = '2023'   # end of date range
                        
                        # Step 3: Fetch data using the custom connection
                        dataframes_dict = connection.query(seriesids_list,
                                                           start_year_str, 
                                                           end_year_str,
                                                           api_key = None)
                        
                        # Step 4: Create dataframes
                        gas_df = dataframes_dict['APU000074714']
                        electricity_df = dataframes_dict['APU000072610']
                        
                        # Step 5: Show Dataframes in Streamlit
                        st.dataframe(gas_df)
                        st.dataframe(electricity_df)
                        '''

                # Show codeblock in Streamlit
                st.code(code, language='python')
                
                # show note to user in Streamlit
                my_text_paragraph('''*Series ID's can be retrieved from the <a href="https://beta.bls.gov/dataQuery/search" target="_blank">U.S. Bureau of Labor Statistics</a>''', my_font_size = '16px')
                
                vertical_spacer(2)      
                
                col1, col2, col3 = st.columns([3, 2, 2])
                with col2:                
                    st.caption('powered by')                  
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
         
                    #st.image('./images/streamlit-logo-secondary-colormark-darktext.png') # just the streamlit logo 
                    # clickable streamlit logo with hyperlink to website
                    # requirements:
                    # 1. image located in static folder
                    # 2. config.toml has added: [server] and on newline: enableStaticServing = true
                    # source: https://docs.streamlit.io/library/advanced-features/static-file-serving
                    st.markdown('<a href="https://streamlit.io" target="_blank"><img src="./app/static/streamlit_logo.png" width="268"></a>', unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 8, 1])
                with col2:
                    #st.image('./images/logo_small.svg', use_column_width=True)
                    st.markdown('<a href="https://pypi.org/project/streamlit-bls-connection/" target="_blank"><img src="./app/static/logo.png" width="450"></a>', unsafe_allow_html=True)
    # Disclaimer
    with tab6:
        with st.expander('', expanded=True):
            vertical_spacer(1) #linebreak
            my_text_header('Disclaimer', my_font_size='48px', my_font_family='Poiret One')
            col1, col2, col3 = st.columns([1, 10, 1])
            with col2:
                vertical_spacer(2) #linebreaks 2x
                my_text_paragraph('''The gasoline, diesel, electricity prices and comparison displayed on this app are for <b><span style="color: #456cff;">informational purposes</span></b> only. 
                                  Data sourced from the U.S. Bureau of Labor Statistics (BLS.gov) is provided <b><span style="color: #456cff;">without any warranty or guarantee</span></b>  of <b><span style="color: #456cff;">accuracy</span></b> or <b><span style="color: #456cff;">reliability</span></b>. 
                                  The creator does <b><span style="color: #456cff;">not</span></b> provide financial, investment, or consumption advice. Users are advised to verify the data from official sources and seek professional advice before making any financial or consumption-related decisions. 
                                  By using this app, <b><span style="color: #456cff;">you agree</span></b> that the creator shall <b><span style="color: #456cff;">not</span></b> be held liable for any actions or decisions based on the information provided. Use this app at your own discretion. <b><span style="color: #6f6f74; font-family: Permanent Marker;">Thank you for your understanding!</span></b>
                                  ''', my_text_align='justify')
            col1, col2, col3 = st.columns([2,8,2])
            with col2:
                vertical_spacer(4) #linebreaks 4x
                st.image('./images/disclaimer_logo.png')
                vertical_spacer(6) #linebreaks 6x
                
if __name__ == "__main__":
    main()
