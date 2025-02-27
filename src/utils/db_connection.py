import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import URL

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_SCHEMA, POSTGRES_PORT, DB_HOST

connection = psycopg2.connect(
    dbname=POSTGRES_DB,   
    user=POSTGRES_USER,          
    password=POSTGRES_PASSWORD,      
    host=DB_HOST,              
    port=POSTGRES_PORT,
    options=f'-c search_path={POSTGRES_SCHEMA}' 
)    

engine = create_engine(
        URL.create(        
        "postgresql+psycopg2",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,  
        host=DB_HOST,
        database=POSTGRES_DB),
        connect_args={"search_path": POSTGRES_SCHEMA}
        )


cur = connection.cursor()

# Example query: Get the number of rows in a table
cur.execute("SELECT * FROM tour_data_processed_0701 LIMIT(100);") 

# Fetch the result
row_count = cur.fetchone()
print(f"Number of rows in the table: {row_count}")

# Close the cursor and connection
cur.close()
connection.close()
