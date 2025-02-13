import pandas as pd
from decouple import config
from sqlalchemy import create_engine, exc
from sqlalchemy_utils import database_exists, create_database
import logging
# Importing data transformation functions from separate modules
from data_transformations import (
    transform_movies, transform_shows, transform_genres, transform_production_countries,
    transform_actors, transform_directors, transform_characters, transform_imdb_info
)
from database_models import Base
from data_utils import data_to_sql
from data_view import create_view

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(filename='data_log.log', level=logging.INFO)

    try:
        # Load environment variables
        CONNECTION_STRING = config('CONNECTION_STRING')
        logging.info("Loaded environment variables.")

        # Create a database engine
        engine = create_engine(CONNECTION_STRING)
        logging.info("Created database engine.")

        # If the database doesn't exist, create it
        if not database_exists(engine.url):
            create_database(engine.url)
            logging.info("Database created.")
        else:
            logging.info("Database already exists.")

        # Load CSV data into pandas DataFrames
        titles = pd.read_csv('../datasets/raw_titles.csv')
        logging.info("Loaded titles dataset.")
        print("Titles dataset sample: \n", titles.head(3))

        credits = pd.read_csv('../datasets/raw_credits.csv')
        logging.info("Loaded credits dataset.")
        print("Credits dataset sample: \n", credits.head(3))

        # Enable copy-on-write mode to avoid modifying original DataFrames
        pd.options.mode.copy_on_write = True

        # Create database tables based on the defined schema
        Base.metadata.create_all(engine)
        logging.info("Created database tables based on schema.")

        # Transform data and insert it into the respective tables
        movies = transform_movies(titles)
        shows = transform_shows(titles)
        genres, genres_bridge = transform_genres(titles)
        production_countries, production_countries_bridge = transform_production_countries(titles)
        actors, actors_bridge = transform_actors(credits)
        directors, directors_bridge = transform_directors(credits)
        characters, characters_bridge = transform_characters(credits)
        imdb_info = transform_imdb_info(titles)
        logging.info("Transformed data.")

        # List of dataframes and their corresponding table names for insertion
        data_table_pairs = [
            (movies, 'movies'),
            (shows, 'shows'),
            (genres, 'genres'),
            (genres_bridge, 'genres_bridge'),
            (production_countries, 'production_countries'),
            (production_countries_bridge, 'production_countries_bridge'),
            (actors, 'actors'),
            (actors_bridge, 'actors_bridge'),
            (directors, 'directors'),
            (directors_bridge, 'directors_bridge'),
            (characters, 'characters'),
            (characters_bridge, 'characters_bridge'),
            (imdb_info, 'imdb_info')
        ]

        # Loop through each pair and call data_to_sql function for data insertion
        for data, table in data_table_pairs:
            try:
                data_to_sql(data, table, engine)
                logging.info(f"Inserted data into {table} table.")
            except exc.SQLAlchemyError as e:
                logging.error(f"Error inserting data into {table} table: {e}")

        create_view(engine)
        logging.info("View 'movies_and_shows_view' created successfully.")

        # Close the connection and dispose of all associated resources
        engine.dispose()
        logging.info("Database connection closed and resources disposed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        logging.shutdown()  # Ensure all buffered logs are flushed to disk