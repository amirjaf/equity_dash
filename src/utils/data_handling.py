import pandas

# CONSTANTS
PERSON_WEIGHT = 'psexpfac'

def filter_df(df, conditions):
    """
    Filters a DataFrame based on a dictionary of conditions.

    Parameters:
        df (pd.DataFrame): The DataFrame to filter.
        conditions (dict): A dictionary where keys are column names and values are filter criteria.
    
    Returns:
        pd.DataFrame: The filtered DataFrame.

    Example:
        filter_df(tour_data, {'ocounty':5, 'tourmode2':3})
    """
    filtered_df = df.copy()
    for column, value in conditions.items():
        if isinstance(value, (list, tuple)):
            # Filter with multiple values
            filtered_df = filtered_df[filtered_df[column].isin(value)]
        else:
            # Filter with a single value
            filtered_df = filtered_df[filtered_df[column] == value]
    return filtered_df



def cross_tab(df, var1, var2):
    """
    Creates a pivot table (cross-tabulation) for two variables in the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        var1 (str): The name of the first variable (rows of the pivot table).
        var2 (str): The name of the second variable (columns of the pivot table).
    
    Returns:
        pd.DataFrame: A pivot table with counts for the cross-tabulation.
    Example:
        cross_tab(df, RACE, MODE)
    """
    pivot_table = pandas.pivot_table(
        df,
        values=PERSON_WEIGHT,  
        index=var1,   
        columns=var2, 
        aggfunc='sum', 
        fill_value=0  
    )
    pivot_table_sorted = pivot_table.sort_index(axis=0)  # Sort rows numerically
    pivot_table_sorted = pivot_table_sorted.sort_index(axis=1)
    return pivot_table_sorted

def group_to_dict(df, var1, var2):
    """
    Groups the DataFrame by one column and aggregates another column into lists.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        var1 (str): The column to group by.
        var2 (str): The column to aggregate into lists.
    
    Returns:
        dict: A dictionary where keys are unique values of var1 and values are lists of corresponding var2 values.

    Example:
        df = pd.DataFrame({'A': [1, 1, 2], 'B': ['x', 'y', 'z']})
        group_to_dict(df, 'A', 'B') 
        # Output: {1: ['x', 'y'], 2: ['z']}
    """
    return df.groupby(var1)[var2].apply(list).to_dict()

