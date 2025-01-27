# package imports
import dash
import dash_bootstrap_components as dbc

# local imports
from components.pie_chart_AIO import PieChartAIO
from components.line_chart_AIO import LineChartAIO

dash.register_page(

    __name__,
    path='/trip_based/page_income',
    title='Income Analysis'
)

# load the processed tour file
from .load_trip_data import trip_df

dropdowns_pie_charts = {
    'dpurp2': {
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
    'RACE': {
        'label': 'Race',
        'options': [

            {'label': 'All Race', 'value': 'all'},
            {'label': 'White Race', 'value': 1},
            {'label': 'African American Race', 'value': 2},
            {'label': 'Asian Race', 'value': 3},
            {'label': 'Others Race', 'value': 4},
        ]

    }
}

pivots_pie_charts = {
    'index': {
        'attribute': 'lowinc',
        'labels': {  
            1: 'Above 2x Poverty Line',
            2: 'Above Poverty Line',
            3: 'Below Poverty Line',
        }
    },
    'column': {
        'attribute': 'tripmode',
        'labels': {  
            1: 'SOV',
            2: 'HOV2',
            3: 'HOV3+',
            5: 'Transit',
            6: 'Bike',
            7: 'Walk',
            8: 'School Bus',
        }
    }
}

dropdowns_distribution = {
    'dpurp2': {
        'label': 'Purpose',
        'options': [
            {'label': 'Work', 'value': 1},
            {'label': 'School', 'value': 2},
            {'label': 'Others', 'value': 3},
        ]

    },
    'tripmode2': {
        'label': 'Trip Mode',
        'options': [
            {'label': 'Auto (SOV, HOV2, HOV3+)', 'value': 1},
            {'label': 'Transit (Walk To Transit, Drive To Transit)', 'value': 2},
            {'label': 'Active (Walk, Bike)', 'value': 3},
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

pivots_dist_distance = {
    'index': {
        'attribute': 'lowinc',
        'labels': {  
            1: 'Above 2x Poverty Line',
            2: 'Above Poverty Line',
            3: 'Below Poverty Line',
        }
    },
    'column': {
        'attribute': 'travdist',
        'labels': {  # continues variable
        }
    }
}

pivots_dist_duration = {
    'index': {
        'attribute': 'lowinc',
        'labels': {  
            1: 'Above 2x Poverty Line',
            2: 'Above Poverty Line',
            3: 'Below Poverty Line',
        }
    },
    'column': {
        'attribute': 'ttravtime',
        'labels': {  # continues variable
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
                    dropdowns=dropdowns_pie_charts,
                    pivot_elements=pivots_pie_charts, # pivot table index and columns
                    activity_type='Trip', # default is Travel
                    aio_id='inc_mode_share_trip'
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
                    dropdowns=dropdowns_distribution,
                    pivot_elements=pivots_dist_distance, # pivot table index and columns
                    kind='Distance',
                    activity_type='Trip',
                    aio_id='income_distance_distribution_trip'
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
                    dropdowns=dropdowns_distribution,
                    pivot_elements=pivots_dist_duration, # pivot table index and columns
                    kind='Duration',
                    activity_type='Trip',
                    aio_id='income_travel_time_distribution_trip'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space after the third row
        ),
    ],
    fluid=True
)
