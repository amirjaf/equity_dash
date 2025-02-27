# package imports
import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

layout = html.Div(
    style={
        "font-family": "Arial, sans-serif",
        "margin": "20px",
        "padding": "20px",
        "background-color": "#f9f9f9",
        "border-radius": "8px",
        "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    },
    children=[
        # Header
        html.H1(
            "Welcome To DVRPC Equity Dashboard!",
            style={
                "text-align": "left",
                "color": "#0078ae",
                "margin-bottom": "20px"
            }
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
                "margin-left": "0"  # Align the paragraph with the left side
            }
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
                    }
                )
            ],
            style={"margin-bottom": "20px"}
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
                    }
                )
            ],
            style={"margin-bottom": "20px"}
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
                        "margin-top": "10px"
                    }
                )
            ],
            style={
                "text-align": "center",
                "margin-top": "40px",
                "padding": "10px",
                "border-top": "1px solid #ddd",
                "color": "#555",
                "font-size": "16px"
            }
        )
    ]
)
