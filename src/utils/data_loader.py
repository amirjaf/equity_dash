# notes
'''
This file is used for handling anything data (csv) related. 
It can also be used as the pre-processing step.
'''

# package imports
import pandas
import os

def get_tour_data():
    cwd = os.getcwd()
    data_path = os.path.join(cwd, 'src', 'assets', 'data', 'tour_data_processed_0701.csv')
    needed_columns = ['RACE', 'tourmode', 'psexpfac', 'pdpurp2', 'pdpurp', 'ocounty', 'HISP_B', 'lowinc','distcat', 'tautodist','distcat', 'tourmode2', 'timecat2', 'ttravtime']
    df = pandas.read_csv(data_path, usecols=needed_columns, memory_map=True)
    df = df[df['tourmode']!=0] # remove 'other' mode
    df['lowinc'] = df['lowinc'] + 1 # I need my categories to start from 1. to be able to get the correct title name for the graphs. 
    df['HISP_B'] = df['HISP_B'] + 1 # I need my categories to start from 1. to be able to get the correct title name for the graphs. 
    return df
