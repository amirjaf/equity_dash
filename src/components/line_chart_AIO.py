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
        def __init__(self, parent_class_name):
            self.parent_class_name = parent_class_name

        def generate(self, subcomponent, aio_id):
            return {
                'component': self.parent_class_name,
                'subcomponent': subcomponent,
                'aio_id': aio_id
            }

    def __init__(self, df, dropdowns, pivot_elements, kind='Distance', activity_type='Travel', aio_id=None):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        self.aio_id = aio_id
        self.activity_type = activity_type
        self.df = df
        self.dropdowns = dropdowns
        self.index_name = pivot_elements['index']['attribute']
        self.index_labels = pivot_elements['index']['labels']
        self.column_name = pivot_elements['column']['attribute']
        self.column_labels = pivot_elements['column']['labels']
        self.kind = kind
        # unit mapping
        unit_mapping = {
            'Distance': '(miles)',
            'Duration': '(minutes)'
        }

        self.unit = unit_mapping.get(self.kind, '?')

        # initiate the id generator
        self.ids_instance = LineChartAIO.ids(self.__class__.__name__)
        # initiate id for the store and output in the front end html
        self.store_id = self.ids_instance.generate('store', self.aio_id)
        self.output_histogram_id = self.ids_instance.generate('output_histogram', self.aio_id)
        self.output_table_id = self.ids_instance.generate('output_table', self.aio_id)

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
                                html.H1(f"{self.activity_type} {self.kind} Distribution", style={'text-align': 'left'}),
                                html.P(f"{self.kind} between {'home' if self.activity_type.lower()=='tour' else 'origin'} and the {'primary' if self.activity_type.lower()=='tour' else ''} destination", style={'text-align': 'left', 'color': '#0078ae'}),
                                # Group the dropdowns together with titles
                                *self.generate_dropdowns(self.dropdowns),                                
                                # Row for Scatter Chart and Table
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                id=self.output_histogram_id,
                                                children=[],
                                                style={'margin-top': '30px'}
                                            ),
                                            width=9
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                id=self.output_table_id,
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
                    dcc.Store(self.store_id, data=[])
                ],
                style=component_style,
                className="container-fluid",
            )
        )


        # register the callbacks here
        self.register_callbacks()

    def generate_dropdowns(self, dropdown_dict):
        return [
            dbc.Row(
                [
                    dbc.Col(html.Label(f"{self.activity_type} {dropdown['label']}:", style={'font-weight': 'bold'}), width=12),
                    dbc.Col(
                        dcc.Dropdown(
                            id=self.ids_instance.generate(key, self.aio_id),
                            options=dropdown['options'],
                            placeholder=f"Choose the {dropdown['label'].lower()}",
                            value=dropdown['options'][0]['value']
                        ),
                        width=6,
                    ),
                ],
                style={'margin-bottom': '15px'}
            )
            for key, dropdown in dropdown_dict.items()
        ]

    # methods
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

    def create_kde_graph(self, kde_dict, opacity=0.5):
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
                name=f"{self.index_labels[category]}"  # Display the name in the legend
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
                    html.Td(f"{self.index_labels[category]}"),
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
    def make_line_graph(self, dict, var1, var2, _id):
        dict = self.data_processing(dict, var1, var2)
        return self.create_kde_graph(self.creat_kde_xy(dict))

    @cache.memoize()
    def make_table(self, dict, var1, var2, _id):
        dict = self.data_processing(dict, var1, var2)
        return self.create_average_table(dict)

    def register_callbacks(self):
        @callback(
            Output(self.store_id, 'data'),
            [Input(self.ids_instance.generate(key, self.aio_id), 'value') for key in self.dropdowns.keys()]
        )
        def compute_value(*values):
            dropdown_values = dict(zip(self.dropdowns.keys(), values))
            state_data = {
                'filters': dropdown_values,
                'row_name': self.index_name,
                'column_name': self.column_name,
            }
            self.make_line_graph(state_data['filters'], state_data['row_name'], state_data['column_name'], self.aio_id)
            self.make_table(state_data['filters'], state_data['row_name'], state_data['column_name'], self.aio_id)
            return state_data

        @callback(
            Output(self.output_histogram_id, 'children'),
            Output(self.output_table_id, 'children'),
            Input(self.store_id, 'data')
        )
        def update_graph(data):
            return (
                self.make_line_graph(data['filters'], data['row_name'], data['column_name'], self.aio_id), 
                self.make_table(data['filters'], data['row_name'], data['column_name'], self.aio_id)
            )