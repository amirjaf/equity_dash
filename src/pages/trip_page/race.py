# package imports
import dash
import dash_bootstrap_components as dbc

# local imports
from components.pie_chart_AIO import PieChartAIO
from components.line_chart_AIO import LineChartAIO

dash.register_page(
    __name__,
    path='/trip_based/page_race',
    title='Race Analysis'
)

# load the processed tour file
from .load_trip_data import trip_df

# Layout
layout = dbc.Container(
    [
        # First chart - PieChartAIO
        dbc.Row(
            dbc.Col(
                PieChartAIO(
                    trip_df,
                    row_name='RACE',
                    column_name='tourmode',
                    row_list=['White Race', 'Black Race', 'Asian Race', 'Others Race'],
                    column_list=['SOV', 'HOV2', 'HOV3+', 'Transit', 'Bike', 'Walk', 'School Bus'],
                    input_custom_name='Income Level',
                    input_custom_column_name='lowinc',
                    input_custom_list=['Above 2x Poverty Line', 'Above Poverty Line', 'Below Poverty Line'],
                    aio_id='race_mode_share_trip'
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
                    row_name='RACE',
                    column_name='travdist',
                    row_list=['White Race', 'Black Race', 'Asian Race', 'Others Race'],
                    input_custom_name='Income Level',
                    input_custom_column_name='lowinc',
                    input_custom_list=['Above 2x Poverty Line', 'Above Poverty Line', 'Below Poverty Line'],
                    kind='Distance',
                    aio_id='race_distance_distribution_trip'
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
                    row_name='RACE',
                    column_name='ttravtime',
                    row_list=['White Race', 'Black Race', 'Asian Race', 'Others Race'],
                    input_custom_name='Income Level',
                    input_custom_column_name='lowinc',
                    input_custom_list=['Above 2x Poverty Line', 'Above Poverty Line', 'Below Poverty Line'],
                    kind='Duration',
                    aio_id='race_travel_time_distribution_trip'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space after the third row
        ),
    ],
    fluid=True
)
