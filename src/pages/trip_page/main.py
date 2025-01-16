# notes
'''
NOTE: 
This page is only available when explicitly search for /tour_based and it redirects to the tour_based/race_page. 
The tour_based/race_page loads directly as the first page in the tour-based tab, bypassing a main page
and redirection. 
'''
# package imports
from dash import html, dcc, callback, Input, Output
import dash
import dash_bootstrap_components as dbc
import os

# local imports
from utils.data_loader import get_tour_data
from utils.data_handling import filter_df, cross_tab
from components.pie_chart_AIO import PieChartAIO

# Register the page for '/tour_based'
dash.register_page(
    __name__,
    path='/trip_based',
    title='Trip Based'
)

# Layout for '/tour_based' with a redirection to '/tour_based/mode_share_race'
layout =  dcc.Location(id='url_main_trip_page', refresh=True),  # Ensure refresh=True for the redirection



# Callback to handle the redirection from '/tour_based' to '/tour_based/mode_share_race'
@callback(
    Output('url_main_trip_page', 'href'),  # Change the URL path to trigger the redirect
    Input('url_main_trip_page', 'pathname')  # Listen for the pathname change
)
def redirect_to_mode_share_race(pathname):
    # If the user accesses '/trip_based', automatically redirect to '/trip_based/mode_share_race'
    if pathname == '/trip_based':
        return '/trip_based/page_race'
    return pathname  # Keep the current path if it's not '/tour_based'


