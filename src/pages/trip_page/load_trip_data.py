# notes
'''
This file is for creating loading the tour dataframe to prevent re-load it for each page.
'''
# local imports
from utils.data_loader import get_trip_data

# load the processed trip file
trip_df = get_trip_data()


