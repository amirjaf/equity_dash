# package imports
import dash
import dash_bootstrap_components as dbc

# local imports
from components.pie_chart_AIO import PieChartAIO
from components.line_chart_AIO import LineChartAIO

dash.register_page(

    __name__,
    path='/trip_based/page_hispanic',
    title='Hispanic Analysis'
)

# load the processed tour file
from .load_trip_data import trip_df

dropdowns_pie_charts = {
    'pdpurp2': {
        'label': 'Purpose',
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
        'attribute': 'HISP_B',
        'labels': {  
            1: 'Non-hispanic',
            2: 'Hispanic',
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
                    trip_df,
                    row_name='HISP_B',
                    column_name='tourmode',
                    row_list=['Non-hispanic', 'Hispanic'],
                    column_list=['SOV', 'HOV2', 'HOV3+', 'Transit', 'Bike', 'Walk', 'School Bus'],
                    dropdowns=dropdowns_pie_charts,
                    pivot_elements=pivots_pie_charts, # pivot table index and columns
                    activity_type='Trip', # default is Travel
                    aio_id='hisp_mode_share_trip'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space between rows
        ),
        
        # Second chart - LineChartAIO (Distance)
        dbc.Row(
            dbc.Col(
                LineChartAIO(
                    trip_df,
                    row_name='HISP_B',
                    column_name='travdist',
                    row_list=['Non-hispanic', 'Hispanic'],
                    input_custom_name='Income Level',
                    input_custom_column_name='lowinc',
                    input_custom_list=['Above 2x Poverty Line', 'Above Poverty Line', 'Below Poverty Line'],
                    kind='Distance',
                    aio_id='hisp_distance_distribution_trip'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space after the second row
        ),
        
        # Third chart - LineChartAIO (Travel Time)
        dbc.Row(
            dbc.Col(
                LineChartAIO(
                    trip_df,
                    row_name='HISP_B',
                    column_name='ttravtime',
                    row_list=['White Race', 'African American Race', 'Asian Race', 'Others Race'],
                    input_custom_name='Income Level',
                    input_custom_column_name='lowinc',
                    input_custom_list=['Above 2x Poverty Line', 'Above Poverty Line', 'Below Poverty Line'],
                    kind='Duration',
                    aio_id='hisp_travel_time_distribution_trip'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space after the third row
        ),
    ],
    fluid=True
)


