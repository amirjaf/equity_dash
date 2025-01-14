# notes
'''
This file is for housing the main dash application.
This is where we define the various css items to fetch as well as the layout of our application.
'''

# package imports
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask import Flask
from flask_login import LoginManager
import os
from dash import Input, Output, callback


# local imports
from utils.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK
from components import navbar, footer
from components.navbar_vertical import navbar_vertical

from server import server
dash_app = dash.Dash(
    __name__,
    server=server,
    use_pages=True,    # turn on Dash pages
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ],  # fetch the proper css items we want
    meta_tags=[
        {   # check if device is a mobile device. This is a must if you do any mobile styling
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        }
    ],
    suppress_callback_exceptions=True,
    title='Dash app structure'
)

server.config.update(SECRET_KEY=os.getenv('SECRET_KEY'))

# Login manager object will be used to login / logout users
# login_manager = LoginManager()
# login_manager.init_app(server)
# login_manager.login_view = '/login'

# @login_manager.user_loader
# def load_user(username):
#     """This function loads the user by user id. Typically this looks up the user from a user database.
#     We won't be registering or looking up users in this example, since we'll just login using LDAP server.
#     So we'll simply return a User object with the passed in username.
#     """
#     return User(username)

def serve_layout():
    '''Define the layout of the application'''
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),  # Tracks the current URL
            navbar,  # Horizontal navbar visible on all pages
            html.Div(
                id="vertical-navbar-container",  # Vertical navbar container
                style={
                    # "display": "block", # no need to define. it fills from the callbacks                   
                },
            ),
            html.Div(
                dash.page_container,  # Page-specific content managed by Dash
                style={
                    "marginLeft": "250px",  # Offset the content to make room for the vertical navbar
                    "padding": "1rem",  # Padding for the content area
                    "height": "calc(100vh - 60px)",  # Full height minus the horizontal navbar height
                    "overflowY": "auto",  # Allow scrolling for content when needed
                    "position": "relative",  # Ensure content scrolls without affecting navbar position
                    "paddingTop": "60px",  # Offset for the horizontal navbar height
                },
            ),
            footer,  # Footer for all pages
        ],
        style={
            "height": "100vh",  # Full height for the page container
            "overflow": "hidden",  # Disable page-level scrolling
            "marginTop": "0",  # No margin on the parent container (already handled by navbar and content)
        },
    )


@callback(
    Output("vertical-navbar-container", "style"),
    Output("vertical-navbar-container", "children"),
    Input("url", "pathname"),
)
def toggle_vertical_navbar(pathname):
    # Show vertical navbar only for the 'tour_based' page and redirect to '/tour_based/mode_share_race'
    if pathname.startswith("/tour_based"):
        return {
            "display": "block"  # Ensure the navbar is displayed
        }, navbar_vertical  # Redirect to the desired page
    else:
        return {"display": "none"}, "" # Hide the vertical navbar on other pages


dash_app.layout = serve_layout   # set the layout to the serve_layout function
server = dash_app.server         # the server is needed to deploy the application

if __name__ == "__main__":
    dash_app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK
    )
