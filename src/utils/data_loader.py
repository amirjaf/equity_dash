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
    data_path = os.path.join(cwd, 'src', 'assets', 'data', 'tour_data_processed_0701.pkl')
    needed_columns = ['RACE', 'tourmode', 'psexpfac', 'pdpurp2', 'pdpurp', 'ocounty', 'HISP_B', 'lowinc','distcat', 'tautodist','distcat', 'tourmode2', 'timecat2', 'ttravtime']
    df = pandas.read_pickle(data_path)
    df = df[needed_columns] # make sure all columns are available
    df = df[df['tourmode']!=0] # remove 'other' mode
    df['lowinc'] = df['lowinc'] + 1 # I need my categories to start from 1. to be able to get the correct title name for the graphs. 
    df['HISP_B'] = df['HISP_B'] + 1 # I need my categories to start from 1. to be able to get the correct title name for the graphs. 
    return df

def get_trip_data():
    cwd = os.getcwd()
    data_path = os.path.join(cwd, 'src', 'assets', 'data', 'trip_data_processed_0701.pkl')
    needed_columns = ['RACE', 'tripmode', 'psexpfac', 'dpurp2', 'dpurp', 'ocounty', 'HISP_B', 'lowinc','distcat', 'travdist','distcat', 'tripmode2', 'timecat2', 'ttravtime']
    df = pandas.read_pickle(data_path)
    df = df[needed_columns] # make sure all columns are available
    df = df[df['tripmode']!=0] # remove 'other' mode
    df['lowinc'] = df['lowinc'] + 1 # I need my categories to start from 1. to be able to get the correct title name for the graphs. 
    df['HISP_B'] = df['HISP_B'] + 1 # I need my categories to start from 1. to be able to get the correct title name for the graphs. 
    return df
