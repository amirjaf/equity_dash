# notes
'''
This file is for creating a vertical navigation bar.
'''

# package imports
from dash import html
import dash_bootstrap_components as dbc

# component
navbar_vertical_tour_page = dbc.Container(
    [
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Race", href="/tour_based/page_race", style={"fontSize": "25px", "padding": "20px", "color": "white"}, active="exact")),
                dbc.NavItem(dbc.NavLink("Hispanic", href="/tour_based/page_hispanic", style={"fontSize": "25px", "padding": "20px", "color": "white"}, active="exact")),
                dbc.NavItem(dbc.NavLink("Income", href="/tour_based/page_income", style={"fontSize": "25px", "padding": "20px", "color": "white"}, active="exact")),
            ],
            vertical=True,
            pills=True,
            className='flex-column',
        ),
    ],
    style={
        'height': '100vh',
        #"height": "calc(100vh - 60px)"
        'width': '200px',
        'backgroundColor': '#343a40',  # Dark background color
        'padding': '1rem',
        'color': 'white',
        "paddingTop": "10px",  # Padding for top content in navbar
        "position": "fixed",  # Fixes the navbar to the left side
        "overflowY": "auto",
        'fontFamily': 'Arial, sans-serif',  # Consistent font family
        
    },
)