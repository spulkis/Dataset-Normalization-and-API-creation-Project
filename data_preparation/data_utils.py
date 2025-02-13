import logging
from sqlalchemy import exc

def data_to_sql(df, table_name, engine):
    """
    Insert DataFrame into an SQL table using SQLAlchemy.

    Parameters:
    df (pd.DataFrame): The DataFrame containing data to be inserted.
    table_name (str): Name of the SQL table to insert into.
    engine (sqlalchemy.engine.Engine): SQLAlchemy engine instance connected to the database.

    Logs any SQLAlchemyError encountered during insertion to 'data_error.log'.
    """
    df.to_sql(table_name, engine, if_exists='append')
    print(f"{df} data inserted successfully.")
