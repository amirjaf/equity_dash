# Notes
'''
- This AIO generates pie chart cards with a dynamic dictionary of dropdowns, 
which act as filters for the data, enabling pivoting based on two distinct variables.
- The number of pie charts created corresponds to the number of entries in the index variable, 
and the number of categories in each chart matches the length of the column list.
- A custom class was implemented to generate unique IDs for each instance, replacing the use of MATCH.

For more information about AIO components, check out the official documentation:
https://dash.plotly.com/all-in-one-components
'''

# Package imports
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import uuid
import plotly.graph_objects as go

# Local imports
from utils.data_loader import get_tour_data
from utils.data_handling import filter_df, cross_tab
from cache import cache


class PieChartAIO(html.Div):
    class ids:
        def __init__(self, parent_class_name):
            self.parent_class_name = parent_class_name

        def generate(self, subcomponent, aio_id):
            return {
                'component': self.parent_class_name,
                'subcomponent': subcomponent,
                'aio_id': aio_id
            }

    def __init__(self, df, dropdowns, pivot_elements, activity_type='Travel', aio_id=None):
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
        

        # initiate the id generator
        self.ids_instance = PieChartAIO.ids(self.__class__.__name__)
        # initiate id for the store and output in the front end html
        self.store_id = self.ids_instance.generate('store', self.aio_id)
        self.output_id = self.ids_instance.generate('output', self.aio_id)

        self.component_style = {
            "font-family": "Arial, sans-serif",
            "margin": "20px",
            "padding": "20px",
            "background-color": "#f9f9f9",
            "border-radius": "8px",
            "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
        }

        self.color_palette = [
            'rgba(31, 119, 180, 1)',  # Blue
            'rgba(255, 127, 14, 1)',  # Orange
            'rgba(44, 160, 44, 1)',   # Green
            'rgba(214, 39, 40, 1)',   # Red
            'rgba(148, 103, 189, 1)', # Purple
            'rgba(140, 86, 75, 1)',   # Brown
            'rgba(227, 119, 194, 1)', # Pink
            'rgba(127, 127, 127, 1)', # Gray
            'rgba(188, 189, 34, 1)',  # Olive
            'rgba(23, 190, 207, 1)'   # Cyan
        ]

        super().__init__(
            html.Div(
                [
                    dbc.Row(
                        dbc.Col(
                            [
                                html.H1(f"{self.activity_type} Mode Share", style={'text-align': 'left'}),
                                *self.generate_dropdowns(self.dropdowns),
                                html.Div(id=self.output_id, children=[], style={'margin-top': '30px'}),
                            ],
                            width=12,
                            style={'height': '100vh', 'padding': '10px'}
                        ),
                        justify='center',
                        align='start',
                    ),
                    dcc.Store(id=self.store_id, data=[])
                ],
                style=self.component_style,
                className="container-fluid",
            ),
        )

        self.register_callbacks()

    def generate_dropdowns(self, dropdown_dict):
        return [
            dbc.Row(
                [
                    dbc.Col(html.Label(f"Select {dropdown['label']}:", style={'font-weight': 'bold'}), width=12),
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

    def pie_charts_grid(self, pie_chart_list):
        return dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        pie_chart,
                        style={
                            "padding": "10px",
                            "border": "1px solid #ddd",
                            "border-radius": "8px",
                            "background-color": "#f9f9f9",
                            "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
                        },
                    ),
                    width=6,
                )
                for pie_chart in pie_chart_list
            ],
            justify="left",
            align="start",
            className="g-4"
        )

    def create_pie_charts(self, table):
        return [
            dcc.Graph(
                figure=self.get_pie_chart_data(row, index),
                id=f'pie-chart-{index}'
            )
            for index, row in table.iterrows()
        ]

    def get_pie_chart_data(self, row, index):
        colors = self.color_palette[:len(self.column_labels)]
        pie_chart = go.Figure(
            data=[
                go.Pie(
                    labels=[self.column_labels[index] for index in row.index],
                    values=row.values,
                    textinfo='label+percent',
                    insidetextorientation='horizontal',
                    hole=0.3,
                    marker=dict(colors=colors)
                )
            ]
        )
        pie_chart.update_layout(
            title=f"{self.index_labels[index]}",
            title_font=dict(family="Arial", size=24, color="black"),
            margin=dict(t=40, b=40, l=0, r=40),
        )
        return pie_chart

    def global_store(self, filters, var1, var2):
        filtered_data = filter_df(self.df, {k: v for k, v in filters.items() if v != 'all'})
        return cross_tab(filtered_data, var1, var2)

    @cache.memoize()
    def make_pie_charts(self, data, _id):
        table = self.global_store(data['filters'], data['row_name'], data['column_name'])
        return self.pie_charts_grid(self.create_pie_charts(table))

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
            self.make_pie_charts(state_data, self.aio_id)
            return state_data

        @callback(
            Output(self.output_id, 'children'),
            Input(self.store_id, 'data')
        )
        def update_graph(data):
            return self.make_pie_charts(data, self.aio_id)
