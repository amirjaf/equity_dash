# notes
'''
This AIO creates pie charts card with two dropdowns for travel purpose and origin county as filters
based on two different variables for pivoting.
I did not use MATCH, created a class for making uniqe ids for each instance.

For more information about AIO components, check out the official documentation:
https://dash.plotly.com/all-in-one-components
'''

# package imports
from dash import html, dcc, callback, Output, Input, MATCH, State
import dash_bootstrap_components as dbc
import uuid
import plotly.graph_objects as go

# local imports
from utils.data_loader import get_tour_data
from utils.data_handling import filter_df, cross_tab
from cache import cache

class PieChartAIO(html.Div):

    class ids:
        store = lambda aio_id: {
            'component': 'PieChartAIO',
            'subcomponent': 'store',
            'aio_id': aio_id
        }
        input_purpose = lambda aio_id: {
            'component': 'PieChartAIO',
            'subcomponent': 'input_purpose',
            'aio_id': aio_id
        }
        input_county = lambda aio_id: {
            'component': 'PieChartAIO',
            'subcomponent': 'input_county',
            'aio_id': aio_id
        }
        input_custom = lambda aio_id: {
            'component': 'PieChartAIO',
            'subcomponent': 'input_custom',
            'aio_id': aio_id
        }
        pie_container = lambda aio_id: {
            'component': 'PieChartAIO',
            'subcomponent': 'pie_container',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(self, df, row_name, column_name, row_list, column_list, input_custom_name, input_custom_column_name, input_custom_list, aio_id=None):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        self.aio_id = aio_id
        self.df = df  # main data frame
        self.row_name = row_name
        self.column_name = column_name
        self.row_list = row_list
        self.column_list = column_list
        self.input_custom_name = input_custom_name # custom dropdown name
        self.input_custom_list = input_custom_list # custom drop down options
        self.input_custom_column = input_custom_column_name

        # Style dictionary
        component_style = {
            "font-family": "Arial, sans-serif",
            "margin": "20px",
            "padding": "20px",
            "background-color": "#f9f9f9",
            "border-radius": "8px",
            "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
        }

        # Layout for the dropdowns and pie charts container
        super().__init__(
            html.Div(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H1("Travel Mode Share", style={'text-align': 'left'}),
                                # Group the dropdowns together with titles
                                dbc.Row(
                                    [
                                        dbc.Col(html.Label("Select Travel Purpose:", style={'font-weight': 'bold'}), width=12),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id=self.ids.input_purpose(self.aio_id),
                                                options=[
                                                    {'label': 'Work', 'value': 1},
                                                    {'label': 'School', 'value': 2},
                                                    {'label': 'Others', 'value': 3},
                                                ],
                                                placeholder="Choose the purpose of travel",
                                                value=1
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    style={'margin-bottom': '15px'}
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.Label("Select Origin County:", style={'font-weight': 'bold'}), width=12),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id=self.ids.input_county(self.aio_id),
                                                options=[
                                                    {'label': 'All Counties', 'value': 'all'},
                                                    {'label': 'Bucks', 'value': 1},
                                                    {'label': 'Chester', 'value': 2},
                                                    {'label': 'Delaware', 'value': 3},
                                                    {'label': 'Montgomery', 'value': 4},
                                                    {'label': 'Philadelphia', 'value': 5},
                                                    {'label': 'Burlington', 'value': 6},
                                                    {'label': 'Camden', 'value': 7},
                                                    {'label': 'Gloucester', 'value': 8},
                                                    {'label': 'Mercer', 'value': 9},
                                                ],
                                                placeholder="Choose the origin county",
                                                value='all'
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    style={'margin-bottom': '15px'}
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.Label(f"Select {self.input_custom_name}:", style={'font-weight': 'bold'}), width=12),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id=self.ids.input_custom(self.aio_id),
                                                options= [
                                                    {'label': f"All {self.input_custom_name}", 'value': 'all'},
                                                    *({'label': name, 'value': idx + 1} for idx, name in enumerate(self.input_custom_list))
                                                ],
                                                placeholder=f"Choose {self.input_custom_name}",
                                                value='all'
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    style={'margin-bottom': '30px'}
                                ),                                
                                # Pie charts container to hold all pie charts
                                html.Div(id=self.ids.pie_container(self.aio_id), children=[], style={'margin-top': '30px'}),
                            ],
                            width=12,
                            style={'height': '100vh', 'padding': '10px'}
                        ),
                        justify='center',
                        align='start',
                        style={'height': '100vh', 'width': '100%'}
                    ),
                    dcc.Store(id=self.ids.store(self.aio_id), data=[])
                ],
                style=component_style
            )
        )

        # register the callbacks here
        self.register_callbacks()

    # methods
    def pie_charts_grid(self, pie_chart_list):
        return dbc.Row(
            [
                dbc.Col(pie_chart, width=6)  # Adjust width based on how many pie charts you want in each row
                for pie_chart in pie_chart_list
            ],
            justify="left",  # Center the pie charts in the row
            align="start"
        )

    def create_pie_charts(self, table):
        pie_charts = []

        # Generate a pie chart for each row (category)
        for index, row in table.iterrows():
            pie_chart = self.get_pie_chart_data(row, index)
            pie_charts.append(dcc.Graph(figure=pie_chart, id=f'pie-chart-{index}'))

        return pie_charts

    def get_pie_chart_data(self, row, index):
        # Prepare data for the pie chart
        row_data = row.values  # Extract the values from the row

        # Create the Pie chart inside a Figure
        pie_chart = go.Figure(
            data=[go.Pie(
                labels=self.column_list,
                values=row_data,
                textinfo='label+percent',
                showlegend=False,  # Show the legend
                insidetextorientation='horizontal',
                legendgroup='mode',
                hole=0.3  # Optional: create a donut chart
            )]
        )

        # Update layout with legend and title
        pie_chart.update_layout(
            title=f"{self.row_list[index-1]}",
            title_font=dict(
                family="Arial",  # Font family
                size=24,         # Font size
                color="black",    # Font color
            ),
            title_x=0,
            title_xanchor="left",
            legend_title="Mode",
            legend=dict(
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.1,
                yanchor="top"
            ),
            margin=dict(t=40, b=40, l=0, r=40)  # Adjust the margin to prevent title overlap
        )

        return pie_chart

    @cache.memoize()
    def global_store(self, filters, var1, var2):
        filters_copy = {
            key: value for key, value in filters.items() if value != 'all'
        }  # Remove all 'all' keys to not filter on them        
        table = cross_tab(filter_df(self.df, filters_copy), var1, var2)
        return table

    @cache.memoize()
    def make_pie_charts(self, data):
        table = self.global_store(data['filters'], data['row_name'], data['column_name'])
        grid_charts = self.pie_charts_grid(self.create_pie_charts(table))
        return grid_charts

    def register_callbacks(self):
        @callback(
            Output(self.ids.store(self.aio_id), 'data'),
            Input(self.ids.input_purpose(self.aio_id), 'value'),
            Input(self.ids.input_county(self.aio_id), 'value'),
            Input(self.ids.input_custom(self.aio_id), 'value')
        )
        def compute_value(purp, ocounty, custom):
            # Prepare the state data structure
            state_data = {
                'filters': {'pdpurp2': purp, 'ocounty': ocounty, self.input_custom_column: custom},
                'row_name': self.row_name,
                'column_name': self.column_name
            }
            self.make_pie_charts(state_data)
            return state_data

        @callback(
            Output(self.ids.pie_container(self.aio_id), 'children'),
            Input(self.ids.store(self.aio_id), 'data')
        )
        def update_graph(data):
            return self.make_pie_charts(data)

