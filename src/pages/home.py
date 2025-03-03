# package imports
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from utils.db_requests import get_table_names
from utils.settings import POSTGRES_SCHEMA

dash.register_page(__name__, path="/", redirect_from=["/home"], title="Home")

table_names = get_table_names(POSTGRES_SCHEMA)
table_names = list(set([table[-4:] for table in table_names]))
default_table = table_names[0] if table_names else None

layout = html.Div(
    style={
        "font-family": "Arial, sans-serif",
        "margin": "20px",
        "padding": "20px",
        "background-color": "#f9f9f9",
        "border-radius": "8px",
        "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
    },
    children=[
        # Header
        html.H1(
            "Welcome To DVRPC Equity Dashboard!",
            style={"text-align": "left", "color": "#0078ae", "margin-bottom": "20px"},
        ),
        # Description
        html.P(
            """
            The DVRPC Equity Dashboard is a comprehensive tool designed to promote 
            equity and inclusion in decision-making processes. It provides detailed 
            insights, visualizations, and analyses to support data-driven strategies 
            that benefit all community members, especially those in underserved areas.
            """,
            style={
                "font-size": "20px",
                "line-height": "1.6",
                "color": "#0078ae",
                "margin-bottom": "20px",
                "max-width": "50%",  # Limit the paragraph width
                "text-align": "left",  # Keep text alignment to the left
                "margin-left": "0",  # Align the paragraph with the left side
            },
        ),
        html.Div(
            children=[
                html.H3(
                    "Scenario Selection:",
                    style={
                        "text-align": "left",
                        "color": "#0078ae",
                        "margin-bottom": "10px",
                    },
                ),
                # Dropdown for table selection
                dbc.Col(
                    dcc.Dropdown(
                        id="scenario-dropdown",
                        options=[
                            {"label": table, "value": table} for table in table_names
                        ],
                        value=default_table,
                        placeholder="Select a scenario",
                    ),
                    width=2,
                ),
            ],
            style={"margin-bottom": "30px"},
        ),
        # Link to another section
        html.Div(
            [
                html.A(
                    "Checkout the tour based equity analysis here",
                    href="/tour_based/page_race",
                    style={
                        "text-decoration": "none",
                        "color": "#ff5722",
                        "font-size": "18px",
                    },
                )
            ],
            style={"margin-bottom": "20px"},
        ),
        html.Div(
            [
                html.A(
                    "Checkout the trip based equity analysis here",
                    href="/trip_based/page_race",
                    style={
                        "text-decoration": "none",
                        "color": "#ff5722",
                        "font-size": "18px",
                    },
                )
            ],
            style={"margin-bottom": "20px"},
        ),
        # Content placeholder
        html.Div(id="content"),
        # Footer
        html.Footer(
            [
                html.A(
                    "Go to DVRPC website.",
                    href="https://www.dvrpc.org/",
                    target="_blank",  # Opens the link in a new tab
                    style={
                        "text-decoration": "none",
                        "color": "#007bff",
                        "font-size": "18px",
                        "margin-top": "10px",
                    },
                )
            ],
            style={
                "text-align": "center",
                "margin-top": "40px",
                "padding": "10px",
                "border-top": "1px solid #ddd",
                "color": "#555",
                "font-size": "16px",
            },
        ),
    ],
)

# # Callback to update stored table value based on dropdown selection
# @callback(
#     Output("selected-table", "data"),
#     Input("scenario-dropdown", "value"),
# )
# def update_selected_table(selected_value):
#     if selected_value:
#         return selected_value
#     return None  # Returning None instead of Exception

# # Callback to update dropdown if stored table value changes
# @callback(
#     Output("scenario-dropdown", "value"),
#     Input("selected-table", "data"),
#     State("scenario-dropdown", "value"),
#     prevent_initial_call=True
# )
# def update_dropdown(current_value, dropdown_value):
#     if dropdown_value != current_value:
#         return current_value
#     return dash.no_update


@callback(
    Output("scenario-dropdown", "value"),
    Output("selected-table", "data"),
    Input("scenario-dropdown", "value"),
    prevent_initial_call=False,
)
def sync_dropdown_and_store(selected_value):
    return selected_value, selected_value  # Sync both components
