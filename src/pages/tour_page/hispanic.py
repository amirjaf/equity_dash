# package imports
import dash
import dash_bootstrap_components as dbc

# local imports
from components.pie_chart_AIO import PieChartAIO
from components.line_chart_AIO import LineChartAIO

dash.register_page(

    __name__,
    path='/tour_based/page_hispanic',
    title='Hispanic Analysis'
)

# load the processed tour file
from .load_tour_data import tour_df


# Layout
layout = dbc.Container(
    [
        # First chart - PieChartAIO
        dbc.Row(
            dbc.Col(
                PieChartAIO(
                    tour_df,
                    row_name='HISP_B',
                    column_name='tourmode',
                    row_list=['Non-hispanic', 'Hispanic'],
                    column_list=['SOV', 'HOV2', 'HOV3+', 'Drive To Transit', 'Walk To Transit', 'Bike', 'School Bus'],
                    aio_id='hisp_mode_share'
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
                    row_name='HISP_B',
                    column_name='tautodist',
                    row_list=['Non-hispanic', 'Hispanic'],
                    kind='Distance',
                    aio_id='hisp_distance_distribution'
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
                    row_name='HISP_B',
                    column_name='ttravtime',
                    row_list=['White Race', 'Black Race', 'Asian Race', 'Others Race'],
                    kind='Duration',
                    aio_id='hisp_travel_time_distribution'
                ),
                width=12  # Full width for all screen sizes
            ),
            className="mb-5"  # Add space after the third row
        ),
    ],
    fluid=True
)


