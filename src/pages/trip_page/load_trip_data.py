# notes
'''
This file is for creating loading the tour dataframe to prevent re-load it for each page.
'''
# local imports
from utils.data_loader import get_tour_data, get_trip_data

# load the processed tour file
tour_df = get_tour_data()
trip_data = get_trip_data()


