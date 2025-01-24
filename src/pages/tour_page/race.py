# package imports
import dash
import dash_bootstrap_components as dbc

# local imports
from components.pie_chart_AIO import PieChartAIO
from components.line_chart_AIO import LineChartAIO

dash.register_page(
    __name__,
    path='/tour_based/page_race',
    title='Race Analysis'
)

# load the processed tour file
from .load_tour_data import tour_df

dropdowns_pie_charts = {
    'pdpurp2': {
        'label': 'Primary Purpose',
        'options': [
            {'label': 'Work', 'value': 1},
            {'label': 'School', 'value': 2},
            {'label': 'Others', 'value': 3},
        ]

    },
    'ocounty': {
        'label': 'Origin County',
        'options': [

            {'label': 'All Counties', 'value': 'all'},
            {'label': 'Bucks', 'value': 1},
            {'label': 'Chester', 'value': 2},
            {'label': 'Delaware', 'value': 3},
            {'label': 'Montgomery', 'value': 4},
            {'label': 'Philadelphia', 'value': 5},
            {'label': 'Burlington', 'value': 6},
            {'label': 'Camden', 'value': 7},
            {'label': 'Gloucester', 'value': 8},
        ]

    },
    'lowinc': {
        'label': 'Income Level',
        'options': [

            {'label': 'All Income Level', 'value': 'all'},
            {'label': 'Above 2x Poverty Line', 'value': 1},
            {'label': 'Above Poverty Line', 'value': 2},
            {'label': 'Below Poverty Line', 'value': 3},
        ]

    }
}

pivots_pie_charts = {
    'index': {
        'attribute': 'RACE',
        'labels': {  
            1: 'White Race',
            2: 'African American Race',
            3: 'Asian Race',
            4: 'Others Race',
        }
    },
    'column': {
        'attribute': 'tourmode',
        'labels': {  
            1: 'SOV',
            2: 'HOV2',
            3: 'HOV3+',
            4: 'Drive To Transit',
            5: 'Walk To Transit',
            6: 'Bike',
            7: 'Walk',
            8: 'School Bus',
        }
    }
}

# Layout
layout = dbc.Container(
    [
        # First chart - PieChartAIO
        dbc.Row(
            dbc.Col(
                PieChartAIO(
                    tour_df,
                    row_name='RACE',
                    column_name='tourmode',
                    row_list=['White Race', 'African American Race', 'Asian Race', 'Others Race'],
                    column_list=['SOV', 'HOV2', 'HOV3+', 'Drive To Transit', 'Walk To Transit', 'Bike', 'Walk', 'School Bus'],
                    dropdowns=dropdowns_pie_charts,
                    pivot_elements=pivots_pie_charts, # pivot table index and columns
                    activity_type='Tour', # default is Travel
                    aio_id='race_mode_share_tour'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space between rows
        ),
        
        # Second chart - LineChartAIO (Distance)
        dbc.Row(
            dbc.Col(
                LineChartAIO(
                    tour_df,
                    row_name='RACE',
                    column_name='tautodist',
                    row_list=['White Race', 'African American Race', 'Asian Race', 'Others Race'],
                    input_custom_name='Income Level',
                    input_custom_column_name='lowinc',
                    input_custom_list=['Above 2x Poverty Line', 'Above Poverty Line', 'Below Poverty Line'],
                    kind='Distance',
                    aio_id='race_distance_distribution_tour'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space after the second row
        ),
        
        # Third chart - LineChartAIO (Travel Time)
        dbc.Row(
            dbc.Col(
                LineChartAIO(
                    tour_df,
                    row_name='RACE',
                    column_name='ttravtime',
                    row_list=['White Race', 'African American Race', 'Asian Race', 'Others Race'],
                    input_custom_name='Income Level',
                    input_custom_column_name='lowinc',
                    input_custom_list=['Above 2x Poverty Line', 'Above Poverty Line', 'Below Poverty Line'],
                    kind='Duration',
                    aio_id='race_travel_time_distribution_tour'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space after the third row
        ),
    ],
    fluid=True
)
