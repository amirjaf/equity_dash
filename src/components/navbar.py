# notes
'''
This file is for creating a navigation bar that will sit at the top of your application.
Much of this page is pulled directly from the Dash Bootstrap Components documentation linked below:
https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
'''

# package imports
from dash import html, callback, Output, Input, dcc, State
import dash_bootstrap_components as dbc

# local imports
from utils.images import logo_encoded, logo_encoded_equity_dash

# Navbar component
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logo_encoded, height="65px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.dvrpc.org/",
                style={
                    "textDecoration": "none",
                    "marginRight": "20px"
                },
            ),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logo_encoded_equity_dash, height="160px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={
                    "textDecoration": "none",
                    "marginRight": "20px"
                },
            ),
            

            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink("Home", href="/", id="nav-home", style={"fontSize": "25px", "padding": "20px", "color": "#0078ae"}, active=False)
                        ),
                        dbc.NavItem(
                            dbc.NavLink("Tour Based", id="nav-tour-based", href="/tour_based/page_race", style={"fontSize": "25px", "padding": "20px", "color": "#0078ae"}, active=False)
                        ),  # Reference to the first tab of the 'tour based' page
                        dbc.NavItem(
                            dbc.NavLink("Trip Based",id="nav-trip-based", href="/trip_based/page_race", style={"fontSize": "25px", "padding": "20px", "color": "#0078ae"}, active=False)
                        ),  # Reference to the first tab of the 'trip based' page
                    ],
                    pills=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]
    ),
    color="light",  # Light background for the navbar
    dark=True,  
    style={
        'height': '105px',  
        'backgroundColor': 'white',  
        'fontFamily': 'Arial, sans-serif',  
    }
)




# Callback to set the active state of navigation links based on the URL
@callback(
    [
        Output('nav-home', 'active'),
        Output('nav-tour-based', 'active'),
        Output('nav-trip-based', 'active'),
    ],
    Input('url', 'pathname')
)
def set_active_link(pathname):
    # This allows the active state to be set for all pages under a specific path
    if pathname.startswith('/tour_based'):
        return False, True, False
    elif pathname.startswith('/trip_based'):
        return False, False, True
    else:  # Default to Home
        return True, False, False

# Callback for toggling the collapse on small screens
@callback(
    Output('navbar-collapse', 'is_open'),
    Input('navbar-toggler', 'n_clicks'),
    State('navbar-collapse', 'is_open'),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open