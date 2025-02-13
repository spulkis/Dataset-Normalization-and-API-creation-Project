import pandas as pd

def transform_movies(dataset):
    """
    Create a DataFrame of movies from the dataset.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies and shows.

    Returns:
        pd.DataFrame: A DataFrame containing information about movies.
    """
    movies = dataset[dataset["type"] == "MOVIE"]
    movies = movies.reset_index(drop=True)
    movies.index = movies.index + 1
    movies.rename(columns={'id': 'movie_id'}, inplace=True)
    movies.drop(columns=['index', 'type', 'genres', 'production_countries', 'seasons', 'imdb_id', 'imdb_score', 'imdb_votes'], inplace=True)
    print('\nMovies df sample: \n', movies.head(3))
    return movies

def transform_shows(dataset):
    """
    Create a DataFrame of shows from the dataset.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies and shows.

    Returns:
        pd.DataFrame: A DataFrame containing information about shows.
    """
    shows = dataset[dataset["type"] == "SHOW"]
    shows = shows.reset_index(drop=True)
    shows.index = shows.index + 1
    shows.rename(columns={'id': 'show_id'}, inplace=True)
    shows.drop(columns=['index', 'type', 'genres', 'production_countries', 'imdb_id', 'imdb_score', 'imdb_votes'], inplace=True)
    print('\nShows df sample: \n', shows.head(3))
    return shows

def transform_genres(dataset):
    """
    Transform genres from the dataset into separate DataFrames for genres and a genres bridge.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies and shows.

    Returns:
        tuple: A tuple containing two DataFrames, one for genres and one for the genres bridge.
    """
    genres_exploded = dataset[['id', 'genres']]

    genres_exploded.loc[:, 'genres'] = genres_exploded['genres'].str.replace(r'\[|\]|\'', '', regex=True)
    genres_exploded.loc[:, 'genres'] = genres_exploded['genres'].apply(lambda x: x.split(', ') if isinstance(x, str) else x)

    genres_exploded = genres_exploded.explode('genres')

    genres = genres_exploded[['genres']].drop_duplicates().reset_index(drop=True)
    genres.index = genres.index + 1
    genres['genre_id'] = genres.index

    genres_bridge = pd.merge(genres_exploded, genres, on='genres', how='left')
    genres_bridge.rename(columns={'index': 'genre_id', 'id': 'title_id'}, inplace=True)
    genres_bridge.rename_axis('index', inplace=True)
    genres_bridge.index = genres_bridge.index + 1
    genres_bridge.drop(columns=['genres'], inplace=True)

    genres_bridge.loc[genres_bridge['title_id'].str.startswith('tm'), 'movie_id'] = genres_bridge['title_id']
    genres_bridge.loc[genres_bridge['title_id'].str.startswith('ts'), 'show_id'] = genres_bridge['title_id']
    genres_bridge.drop(columns=['title_id'], inplace=True)

    genres.drop(columns=['genre_id'], inplace=True)
    genres.rename_axis('genre_id', inplace=True)
    genres.rename(columns={'genres': 'genre'}, inplace=True)

    del genres_exploded
    print('\nGenres df sample: \n', genres.head(3))
    print('\nGenres bridge df sample: \n', genres_bridge.head(3))
    return genres, genres_bridge

def transform_production_countries(dataset):
    """
    Transform production countries from the dataset into separate DataFrames for production countries and a production countries bridge.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies and shows.

    Returns:
        tuple: A tuple containing two DataFrames, one for production countries and one for the production countries bridge.
    """
    production_countries_exploded = dataset[['id', 'production_countries']]

    production_countries_exploded.loc[:, 'production_countries'] = production_countries_exploded['production_countries'].str.replace(r'\[|\]|\'', '', regex=True)
    production_countries_exploded.loc[:, 'production_countries'] = production_countries_exploded['production_countries'].apply(lambda x: x.split(', ') if isinstance(x, str) else x)

    production_countries_exploded = production_countries_exploded.explode('production_countries')

    production_countries = production_countries_exploded[['production_countries']].drop_duplicates().reset_index(drop=True)
    production_countries.index = production_countries.index + 1
    production_countries['country_id'] = production_countries.index

    production_countries_bridge = pd.merge(production_countries_exploded, production_countries, on='production_countries', how='left')
    production_countries_bridge.rename(columns={'index': 'country_id', 'id': 'title_id'}, inplace=True)
    production_countries_bridge.rename_axis('index', inplace=True)
    production_countries_bridge.index = production_countries_bridge.index + 1
    production_countries_bridge.drop(columns=['production_countries'], inplace=True)

    production_countries_bridge.loc[production_countries_bridge['title_id'].str.startswith('tm'), 'movie_id'] = production_countries_bridge['title_id']
    production_countries_bridge.loc[production_countries_bridge['title_id'].str.startswith('ts'), 'show_id'] = production_countries_bridge['title_id']
    production_countries_bridge.drop(columns=['title_id'], inplace=True)

    production_countries.drop(columns=['country_id'], inplace=True)
    production_countries.rename_axis('country_id', inplace=True)
    production_countries.rename(columns={'production_countries': 'country'}, inplace=True)

    del production_countries_exploded
    print('\nProduction countries df sample: \n', production_countries.head(3))
    print('\nProduction countries bridge df sample: \n', production_countries_bridge.head(3))
    return production_countries, production_countries_bridge

def transform_actors(dataset):
    """
    Transform actors from the dataset into a separate DataFrames for actors and a actors bridge.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies, shows, and people.

    Returns:
        tuple: A tuple containing two DataFrames, one for actors and one for the actors bridge.
    """
    actors = dataset[dataset["role"] == "ACTOR"]

    actors_bridge = actors[['id', 'person_id']].reset_index(drop=True)
    actors_bridge.loc[actors_bridge['id'].str.startswith('tm'), 'movie_id'] = actors_bridge['id']
    actors_bridge.loc[actors_bridge['id'].str.startswith('ts'), 'show_id'] = actors_bridge['id']
    actors_bridge.drop(columns=['id'], inplace=True)
    actors_bridge.rename(columns = {'person_id':'actor_id'}, inplace = True)
    actors_bridge.rename_axis('index', inplace=True)
    actors_bridge.index = actors_bridge.index + 1

    actors = actors[['person_id', 'name']].drop_duplicates().reset_index(drop=True)
    actors.index = actors.index + 1
    actors.rename_axis('index', inplace=True)
    actors.rename(columns = {'person_id':'actor_id', 'name':'actor'}, inplace = True)
    print('\nActors df sample: \n', actors.head(3))
    print('\nActors bridge df sample: \n', actors_bridge.head(3))
    return actors, actors_bridge

def transform_directors(dataset):
    """
    Transform directors from the dataset into a separate DataFrames for directors and a directors bridge.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies, shows, and people.

    Returns:
        tuple: A tuple containing two DataFrames, one for directors and one for the directors bridge.
    """
    directors = dataset[dataset['role'] == 'DIRECTOR']

    directors_bridge = directors[['id', 'person_id']].reset_index(drop=True)
    directors_bridge.loc[directors_bridge['id'].str.startswith('tm'), 'movie_id'] = directors_bridge['id']
    directors_bridge.loc[directors_bridge['id'].str.startswith('ts'), 'show_id'] = directors_bridge['id']
    directors_bridge.drop(columns=['id'], inplace=True)
    directors_bridge.rename(columns = {'person_id':'director_id'}, inplace = True)
    directors_bridge.rename_axis('index', inplace=True)
    directors_bridge.index = directors_bridge.index + 1

    directors = directors[['person_id', 'name']].drop_duplicates().reset_index(drop=True)
    directors.index = directors.index + 1
    directors.rename_axis('index', inplace=True)
    directors.rename(columns = {'person_id':'director_id', 'name':'director'}, inplace = True)
    print('\nDirectors df sample: \n', directors.head(3))
    print('\nDirectors bridge df sample: \n', directors_bridge.head(3))
    return directors, directors_bridge

def transform_characters(dataset):
    """
    Transform characters from the dataset into separate DataFrames for characters and a characters bridge.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies, shows, and people.

    Returns:
        tuple: A tuple containing two DataFrames, one for characters and one for the characters bridge.
    """
    characters_exploded = dataset[dataset["role"] == "ACTOR"]
    characters_exploded = characters_exploded[['id', 'person_id', 'character']]

    characters_exploded.loc[:, 'character'] = characters_exploded['character'].str.replace(r'\[|\]|\'', '', regex=True)
    characters_exploded.loc[:, 'character'] = characters_exploded['character'].str.split(' / ')

    characters_exploded = characters_exploded.explode('character')

    characters = characters_exploded[['character']].drop_duplicates().reset_index(drop=True)
    characters.index = characters.index + 1
    characters['character_id'] = characters.index

    characters_bridge = pd.merge(characters_exploded, characters, on='character', how='left')
    characters_bridge.rename(columns={'id': 'title_id', 'person_id': 'actor_id'}, inplace=True)
    characters_bridge.rename_axis('index', inplace=True)
    characters_bridge.index = characters_bridge.index + 1
    characters_bridge.drop(columns=['character'], inplace=True)

    characters_bridge.loc[characters_bridge['title_id'].str.startswith('tm'), 'movie_id'] = characters_bridge['title_id']
    characters_bridge.loc[characters_bridge['title_id'].str.startswith('ts'), 'show_id'] = characters_bridge['title_id']
    characters_bridge.drop(columns=['title_id'], inplace=True)

    characters.drop(columns=['character_id'], inplace=True)
    characters.rename_axis('character_id', inplace=True)

    del characters_exploded
    print('\nCharacters df sample: \n', characters.head(3))
    print('\nCharacters bridge df sample: \n', characters_bridge.head(3))
    return characters, characters_bridge

def transform_imdb_info(dataset):
    """
    Transform IMDB information from the dataset into a separate DataFrame for IMDB info.

    Args:
        dataset (pd.DataFrame): The input dataset containing information about movies and shows.

    Returns:
        pd.DataFrame: A DataFrame containing IMDB information for movies and shows.
    """
    imdb_info = dataset[['id', 'imdb_id', 'imdb_score', 'imdb_votes']]
    imdb_info.loc[imdb_info['id'].str.startswith('tm'), 'movie_id'] = imdb_info['id']
    imdb_info.loc[imdb_info['id'].str.startswith('ts'), 'show_id'] = imdb_info['id']
    imdb_info.rename_axis('index', inplace=True)
    imdb_info.index = imdb_info.index + 1
    imdb_info.drop(columns=['id'], inplace=True)
    print('\nIMDBInfo df sample: \n', imdb_info.head(3))
    return imdb_info
