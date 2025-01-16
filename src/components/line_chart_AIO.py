# Notes
"""
This AIO creates a line chart card with two dropdowns for travel purpose, tour mode type (auto, transit, active), origin county, and a custom dropdown  as filters
based on two different variables for pivoting.
I did not use MATCH, created a class for making unique ids for each instance.

For more information about AIO components, check out the official documentation:
https://dash.plotly.com/all-in-one-components
"""

# Package imports
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import uuid
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy

# Local imports
from utils.data_handling import filter_df, group_to_dict
from cache import cache

class LineChartAIO(html.Div):

    class ids:
        store = lambda aio_id: {
            'component': 'LineChartAIO',
            'subcomponent': 'store',
            'aio_id': aio_id
        }
        input_purpose = lambda aio_id: {
            'component': 'LineChartAIO',
            'subcomponent': 'input_purpose',
            'aio_id': aio_id
        }
        input_county = lambda aio_id: {
            'component': 'LineChartAIO',
            'subcomponent': 'input_county',
            'aio_id': aio_id
        }
        input_mode = lambda aio_id: {
            'component': 'LineChartAIO',
            'subcomponent': 'input_mode',
            'aio_id': aio_id
        }
        input_custom = lambda aio_id: {
            'component': 'LineChartAIO',
            'subcomponent': 'input_custom',
            'aio_id': aio_id
        }
        scatter_container = lambda aio_id: {
            'component': 'LineChartAIO',
            'subcomponent': 'scatter_container',
            'aio_id': aio_id
        }
        table_container = lambda aio_id: {
            'component': 'LineChartAIO',
            'subcomponent': 'table_container',
            'aio_id': aio_id            
        }

    ids = ids

    def __init__(self, df, row_name, column_name, row_list, input_custom_name, input_custom_column_name, input_custom_list, kind='Distance', aio_id=None):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        self.aio_id = aio_id
        self.df = df  # main data frame
        self.row_name = row_name
        self.column_name = column_name
        self.row_list = row_list
        self.input_custom_name = input_custom_name # custom dropdown name
        self.input_custom_list = input_custom_list # custom drop down options
        self.input_custom_column = input_custom_column_name # the name of the column to filter on in the file
        self.kind = kind
        # unit mapping
        unit_mapping = {
            'Distance': '(miles)',
            'Duration': '(minutes)'
        }

        self.unit = unit_mapping.get(self.kind, '?')

        # Style dictionary
        component_style = {
            "font-family": "Arial, sans-serif",
            "margin": "20px",
            "padding": "20px",
            "background-color": "#f9f9f9",
            "border-radius": "8px",
            "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
        }

    # Fixed layout code
        super().__init__(
            html.Div(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H1(f"Tour {self.kind} Distribution", style={'text-align': 'left'}),
                                html.P(f"Tour {self.kind} is the {self.kind.lower()} between home and the primary destination.", style={'text-align': 'left'}),

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
                                        dbc.Col(html.Label("Select Travel Mode:", style={'font-weight': 'bold'}), width=12),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id=self.ids.input_mode(self.aio_id),
                                                options=[
                                                    {'label': 'Auto (SOV, HOV2, HOV3+)', 'value': 1},
                                                    {'label': 'Transit (Walk To Transit, Drive To Transit)', 'value': 2},
                                                    {'label': 'Active (Walk, Bike)', 'value': 3},
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
                                
                                # Row for Scatter Chart and Table
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                id=self.ids.scatter_container(self.aio_id),
                                                children=[],
                                                style={'margin-top': '30px'}
                                            ),
                                            width=9
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                id=self.ids.table_container(self.aio_id),
                                                children=[],
                                                style={'margin-top': '30px'}
                                            ),
                                            width=3
                                        )
                                    ]
                                ),
                            ],
                            width=12,
                            style={'height': '100vh', 'padding': '10px'}
                        )
                    ),
                    dcc.Store(id=self.ids.store(self.aio_id), data=[])
                ],
                style=component_style,
                className="container-fluid",
            )
        )


        # register the callbacks here
        self.register_callbacks()

    # methods
    @cache.memoize()
    def data_processing(self, filters, var1, var2):
        filters_copy = {
            key: value for key, value in filters.items() if value != 'all'
        }  # Remove all 'all' keys to not filter on them        
        filtered_df = filter_df(self.df, filters_copy)[[var1, var2]]
        return group_to_dict(filtered_df, var1, var2)

    def creat_kde_xy(self, dict, bw_method='silverman', bw_adjust=0.3, bin_number=200):
        kde_dict = {}
        for key, numbers in dict.items():
            numbers = numpy.array(numbers)
            kde = gaussian_kde(numbers, bw_method=bw_method)
            kde.set_bandwidth(bw_method=kde.factor * bw_adjust)  # adjust the factor
            x_kde = numpy.linspace(min(numbers), max(numbers), bin_number)
            y_kde = kde(x_kde)
            kde_dict[key] = (x_kde, y_kde)
        return kde_dict

    def create_kde_graph(self, kde_dict, opacity=0.2):
        # Define a high-contrast custom color palette
        color_palette = [
            'rgba(31, 119, 180, {opacity})',  # Blue
            'rgba(255, 127, 14, {opacity})',  # Orange
            'rgba(44, 160, 44, {opacity})',   # Green
            'rgba(214, 39, 40, {opacity})',   # Red
            'rgba(148, 103, 189, {opacity})', # Purple
            'rgba(140, 86, 75, {opacity})',   # Brown
            'rgba(227, 119, 194, {opacity})', # Pink
            'rgba(127, 127, 127, {opacity})', # Gray
            'rgba(188, 189, 34, {opacity})',  # Olive
            'rgba(23, 190, 207, {opacity})'   # Cyan
        ]

        # Assign colors dynamically while ensuring a loop if there are more categories than colors
        category_to_color = {
            i: color_palette[(i-1) % len(color_palette)].format(opacity=opacity)
            for i in kde_dict
        }

        # Prepare the data for the scatter plot
        data = [
            go.Scatter(
                x=kde_dict[category][0],  # kde_x
                y=kde_dict[category][1],  # kde_y
                mode='lines',
                line=dict(width=3.0, color=category_to_color[category]),
                fill='tozeroy',
                fillcolor=category_to_color[category],  # Fill area under curve with the same color
                name=f"{self.row_list[category-1]}"  # Display the name in the legend
            )
            for category in kde_dict
        ]

        # Create the Plotly figure
        figure = go.Figure(
            data=data,
            layout=go.Layout(
                title='KDEs Distribution',
                xaxis={'title': f"{self.kind} {self.unit}"},
                yaxis={'title': 'Density'},
                margin={'l': 60, 'b': 40, 't': 40, 'r': 0}  # Adjust margins for readability
            )
        )
        # Return the figure wrapped inside a dcc.Graph component
        return dcc.Graph(figure=figure)

    def create_average_table(self, dict):
        # Prepare the data for the table
        data = [
            html.Tr(
                [
                    html.Td(f"{self.row_list[category - 1]}"),
                    html.Td(f"{numpy.mean(dict[category]):.2f} {self.unit}")
                ]
            )
            for category in dict
        ]

        # Create the table
        table = dbc.Table(
            [
                # Table Header
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Category"),
                            html.Th(f"Average {self.kind} {self.unit}")
                        ]
                    )
                ),
                # Table Body
                html.Tbody(data)
            ],
            bordered=True,  # Add borders to the table
            hover=True,     # Add hover effect
            responsive=True,  # Make the table responsive
            striped=True,   # Add striped rows for better readability
            style={'margin-top': '0px'}  # Add space above the table
        )

        # Return the table wrapped in a Div for layout purposes
        return html.Div(table, style={'width': '100%'})



    # final function to make the line graph
    @cache.memoize()
    def make_line_graph(self, dict, var1, var2):
        dict = self.data_processing(dict, var1, var2)
        return self.create_kde_graph(self.creat_kde_xy(dict))

    @cache.memoize()
    def make_table(self, dict, var1, var2):
        dict = self.data_processing(dict, var1, var2)
        return self.create_average_table(dict)

    def register_callbacks(self):
        @callback(
            Output(self.ids.store(self.aio_id), 'data'),
            Input(self.ids.input_purpose(self.aio_id), 'value'),
            Input(self.ids.input_mode(self.aio_id), 'value'),
            Input(self.ids.input_county(self.aio_id), 'value'),
            Input(self.ids.input_custom(self.aio_id), 'value')
        )
        def compute_value(purp, mode, ocounty, custom):
            # Prepare the state data structure
            state_data = {
                'filters': {'pdpurp2': purp, 'tourmode2': mode, 'ocounty': ocounty, self.input_custom_column: custom},
                'row_name': self.row_name,
                'column_name': self.column_name
            }
            self.make_line_graph(state_data['filters'], state_data['row_name'], state_data['column_name'])
            self.make_table(state_data['filters'], state_data['row_name'], state_data['column_name'])
            return state_data

        @callback(
            Output(self.ids.scatter_container(self.aio_id), 'children'),
            Output(self.ids.table_container(self.aio_id), 'children'),
            Input(self.ids.store(self.aio_id), 'data')
        )
        def update_graph(data):
            return (
                self.make_line_graph(data['filters'], data['row_name'], data['column_name']), 
                self.make_table(data['filters'], data['row_name'], data['column_name'])
            )