# notes
'''
This file is for creating a vertical navigation bar.
'''

# package imports
from dash import html
import dash_bootstrap_components as dbc

# component
navbar_vertical_trip_page = dbc.Container(
    [
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Race", href="/trip_based/page_race", style={"fontSize": "25px", "padding": "20px", "color": "#0078ae"}, active="exact")),
                dbc.NavItem(dbc.NavLink("Hispanic", href="/trip_based/page_hispanic", style={"fontSize": "25px", "padding": "20px", "color": "#0078ae"}, active="exact")),
                dbc.NavItem(dbc.NavLink("Income", href="/trip_based/page_income", style={"fontSize": "25px", "padding": "20px", "color": "#0078ae"}, active="exact")),
            ],
            vertical=True,
            pills=True,
            className='vertical_navbar',
        ),
    ],
    style={
        'height': '100vh',
        'color': 'white',
        #"height": "calc(100vh - 60px)"
        'width': '200px',
        'backgroundColor': '#cee4f0',  # Dark background color
        #'padding': '1rem',
        'color': 'white',
        "paddingTop": "10px",  # Padding for top content in navbar
        "position": "fixed",  # Fixes the navbar to the left side
        "overflowY": "auto",
        'fontFamily': 'Arial, sans-serif',  # Consistent font family
        
    },
)