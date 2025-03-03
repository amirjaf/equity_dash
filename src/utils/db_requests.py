from sqlalchemy import text
import pandas as pd

from .db_connection import engine

# CONSTANTS
PERSON_WEIGHT = "psexpfac"


def filter_and_pivot(table_name, conditions, var1, var2):
    """
    Filters a SQL table based on conditions and pivots the results.

    Parameters:
        table_name (str): The name of the SQL table. Example: 'tour_data_processed_0701'
        conditions (dict): A dictionary where keys are column names and values are filter criteria. Example: {'ocounty': 5, 'tourmode2': 3}
        var1 (str): Column for pivot rows. Example: 'race'
        var2 (str): Column for pivot columns. Example: 'mode'

    Returns:
        pd.DataFrame: Pivot table with aggregated sums.
                      The index will be `var1`, the columns will be `var2`, and the values will be the sum of `PERSON_WEIGHT`.
    """

    where_clause = " AND ".join([f"{col} = :{col}" for col in conditions])
    where_clause = f"WHERE {where_clause}" if conditions else ""

    sql_query = text(
        f"""
        SELECT {var1}, {var2}, SUM({PERSON_WEIGHT}) AS weight_sum
        FROM {table_name}
        {where_clause} AND {var2} IS NOT NULL
        GROUP BY {var1}, {var2}
    """
    )

    with engine.connect() as conn:
        df = pd.read_sql(sql_query, conn, params=conditions)

    return (
        df.pivot(index=var1, columns=var2, values="weight_sum")
        .sort_index(axis=0)
        .sort_index(axis=1)
        .fillna(0)
    )


def filter_and_list(table_name, conditions, var1, var2):
    """
    Filters a SQL table based on conditions and groups var2 values into lists based on var1.

    Parameters:
        table_name (str): The name of the SQL table. Example: 'tour_data_processed_0701'
        conditions (dict): A dictionary where keys are column names and values are filter criteria. Example: {'ocounty': 5, 'tourmode2': 3}
        var1 (str): The column to group by. Example: 'race'
        var2 (str): The column to aggregate into lists. Example: 'mode'

    Returns:
        dict: A dictionary where keys are unique values of var1 and values are lists of corresponding var2 values.
              Example: {1: ['x', 'y'], 2: ['z']}
    """
    where_clause = " AND ".join([f"{col} = :{col}" for col in conditions])
    where_clause = f"WHERE {where_clause}" if conditions else ""

    sql_query = text(
        f"""
        SELECT {var1}, 
               array_agg({var2}) AS {var2}_values
        FROM {table_name}
        {where_clause}
        GROUP BY {var1}
        ORDER BY {var1}
    """
    )

    with engine.connect() as conn:
        result = conn.execute(sql_query, conditions)
        rows = result.fetchall()

    return {row[0]: row[1] for row in rows}


def get_table_names(schema):
    """
    Get the names of all tables in the database.

    Returns:
        list: A list of table names.
    """
    with engine.connect() as conn:
        result = conn.execute(
            text(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema
            """
            ),
            {"schema": schema},
        )
        return [row[0] for row in result.fetchall()]


if __name__ == "__main__":
    # TEST
    table_name = "tour_data_processed_0701"
    conditions = {"pdpurp2": 1, "ocounty": 5}
    var1 = "race"
    var2 = "tourmode"
    print(filter_and_pivot(table_name, conditions, var1, var2))
    var1 = "race"
    var2 = "tautodist"
    print(filter_and_list(table_name, conditions, var1, var2))
