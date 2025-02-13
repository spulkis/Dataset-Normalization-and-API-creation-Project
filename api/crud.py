from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas 

# Functions related to Movies

def get_movies(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches a list of movies from the database.

    Args:
        db (Session): Database session object.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to fetch.

    Returns:
        List[dict]: List of dictionaries representing movie records.
    """
    return db.query(models.Movies).offset(skip).limit(limit).all()

def get_movies_by_actors(db: Session, actor_name: str, limit: int = 100):
    """
    Fetches movies based on actor name.

    Args:
        db (Session): Database session object.
        actor_name (str): Name of the actor to search for.
        limit (int): Maximum number of records to fetch.

    Returns:
        List[dict]: List of dictionaries representing movie records with actor information.
    """
    query = (
        db.query(
            models.Movies.index,
            models.Movies.movie_id,
            models.Movies.title,
            models.Movies.release_year,
            models.Movies.age_certification,
            models.Movies.runtime,
            models.Actors.actor.label('actor')
        )
        .join(models.ActorsBridge, models.Movies.movie_id == models.ActorsBridge.movie_id)
        .join(models.Actors, models.ActorsBridge.actor_id == models.Actors.actor_id)
        .filter(models.Actors.actor.ilike(f"%{actor_name}%"))  # Case-insensitive search
        .limit(limit)
        .all()
    )

    movies = [
        {
            'movie_id': row.movie_id,
            'title': row.title,
            'release_year': row.release_year,
            'age_certification': row.age_certification,
            'runtime': row.runtime,
            'actor': row.actor,
        }
        for row in query
    ]
    
    return movies

def get_movie_by_ratings(
    db: Session,
    release_year: Optional[int] = None,
    genre: Optional[str] = None,
    limit: int = 1
):
    """
    Fetches movies based on ratings criteria.

    Args:
        db (Session): Database session object.
        release_year (int, optional): Release year of the movie.
        genre (str, optional): Genre of the movie.
        limit (int): Maximum number of records to fetch.

    Returns:
        List[dict]: List of dictionaries representing movie records with rating information.
    """
    query = (
        db.query(
            models.Movies.index,
            models.Movies.movie_id,
            models.Movies.title,
            models.Movies.release_year,
            models.Movies.age_certification,
            models.Movies.runtime,
            models.Genres.genre.label('genre'),
            models.IMDBInfo.imdb_score,
            models.IMDBInfo.imdb_votes
        )
        .join(models.GenresBridge, models.Movies.movie_id == models.GenresBridge.movie_id)
        .join(models.Genres, models.GenresBridge.genre_id == models.Genres.genre_id)
        .join(models.IMDBInfo, models.Movies.movie_id == models.IMDBInfo.movie_id)
    )

    # Apply filters based on the provided parameters
    if release_year is not None:
        query = query.filter(models.Movies.release_year == release_year)
    if genre is not None:
        query = query.filter(models.Genres.genre.ilike(f"%{genre}%"))

    # Sort by imdb_score in descending order
    query = query.order_by(desc(models.IMDBInfo.imdb_score))

    results = query.limit(limit).all()  # Fetch paginated results

    # Convert results to dictionary format with rating information
    movies = [
        {
            "movie_id": result.movie_id,
            "title": result.title,
            "release_year": result.release_year,
            "age_certification": result.age_certification,
            "runtime": result.runtime,
            "genre": result.genre,
            "imdb_score": result.imdb_score,
            "imdb_votes": result.imdb_votes
        }
        for result in results
    ]

    return movies

# Functions related to Shows

from sqlalchemy import desc

def get_shows(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches a list of shows from the database.

    Args:
        db (Session): Database session object.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to fetch.

    Returns:
        List[dict]: List of dictionaries representing show records.
    """
    return db.query(models.Shows).offset(skip).limit(limit).all()

def get_shows_by_details(
    db: Session,
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    age_certification: Optional[str] = None,
    genre: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Fetches shows based on detailed criteria.

    Args:
        db (Session): Database session object.
        title (str, optional): Title of the show.
        release_year (int, optional): Release year of the show.
        age_certification (str, optional): Age certification of the show.
        genre (str, optional): Genre of the show.
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to fetch.

    Returns:
        List[dict]: List of dictionaries representing show records with genre information.
    """
    query = (
        db.query(
            models.Shows.index,
            models.Shows.show_id,
            models.Shows.title,
            models.Shows.release_year,
            models.Shows.age_certification,
            models.Shows.runtime,
            models.Shows.seasons,
            models.Genres.genre.label('genre')
        )
        .join(models.GenresBridge, models.Shows.show_id == models.GenresBridge.show_id)
        .join(models.Genres, models.GenresBridge.genre_id == models.Genres.genre_id)
    )

    # Apply filters based on the provided parameters
    if title is not None:
        query = query.filter(models.Shows.title.ilike(f"%{title}%"))
    if release_year is not None:
        query = query.filter(models.Shows.release_year == release_year)
    if age_certification is not None:
        query = query.filter(models.Shows.age_certification == age_certification)
    if genre is not None:
        query = query.filter(models.Genres.genre.ilike(f"%{genre}%"))

    results = query.offset(skip).limit(limit).all()  # Fetch paginated results

    # Convert results to dictionary format with genre information
    shows = [
        {
            "show_id": result.show_id,
            "title": result.title,
            "release_year": result.release_year,
            "age_certification": result.age_certification,
            "runtime": result.runtime,
            "seasons": result.seasons,
            "genre": result.genre,
        }
        for result in results
    ]

    return shows

def get_media(
    db: Session,
    media_type: str = None,
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    age_certification: Optional[str] = None,
    genre: Optional[str] = None,
    country: Optional[str] = None,
    director: Optional[str] = None,
    actor: Optional[str] = None,
    character: Optional[str] = None,
    imdb_score: Optional[float] = None,
    imdb_votes: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[dict]:
    query = db.query(models.MoviesAndShowsView)
    """
    Fetches media (movies and shows) based on detailed criteria.

    Args:
        db (Session): Database session object.
        media_type (str, optional): Type of media ('movie' or 'show').
        title (str, optional): Title of the movie or show.
        release_year (int, optional): Year of release.
        age_certification (str, optional): Age certification of the media.
        genre (str, optional): Genre of the movie or show.
        country (str, optional): Country of origin.
        director (str, optional): Director of the movie or show.
        actor (str, optional): Lead actor or actress in the movie or show.
        character (str, optional): Character name in the movie or show.
        imdb_score (float, optional): IMDb score of the movie or show.
        imdb_votes (int, optional): Number of IMDb votes for the movie or show.
        skip (int, optional): Number of records to skip (for pagination).
        limit (int, optional): Maximum number of records to fetch.

    Returns:
        List[dict]: List of dictionaries representing media records with genre information.
    """
    
    # Apply filters based on the provided parameters
    if media_type is not None:
        query = query.filter(models.MoviesAndShowsView.media_type.ilike(f"%{media_type}%"))
    if title is not None:
        query = query.filter(models.MoviesAndShowsView.title.ilike(f"%{title}%"))
    if release_year is not None:
        query = query.filter(models.MoviesAndShowsView.release_year == release_year)
    if age_certification is not None:
        query = query.filter(models.MoviesAndShowsView.age_certification == age_certification)
    if genre is not None:
        query = query.filter(models.MoviesAndShowsView.genre.ilike(f"%{genre}%"))
    if country is not None:
        query = query.filter(models.MoviesAndShowsView.country.ilike(f"%{country}%"))
    if director is not None:
        query = query.filter(models.MoviesAndShowsView.director.ilike(f"%{director}%"))
    if actor is not None:
        query = query.filter(models.MoviesAndShowsView.actor.ilike(f"%{actor}%"))
    if character is not None:
        query = query.filter(models.MoviesAndShowsView.character.ilike(f"%{character}%"))
    if imdb_score is not None:
        query = query.filter(models.MoviesAndShowsView.imdb_score > imdb_score)
    if imdb_votes is not None:
        query = query.filter(models.MoviesAndShowsView.imdb_votes > imdb_votes)
    
    results = query.offset(skip).limit(limit).all()  # Fetch paginated results

    # Convert results to dictionary format with genre information
    media = [
        {   
            "movie_id": result.movie_id,
            "show_id": result.show_id,
            "media_type": result.media_type,
            "title": result.title,
            "release_year": result.release_year,
            "age_certification": result.age_certification,
            "runtime": result.runtime,
            "seasons": result.seasons,
            "genre": result.genre,
            "country": result.country,
            "director": result.director,
            "actor": result.actor,
            "character": result.character,
            "imdb_score": result.imdb_score,
            "imdb_votes": result.imdb_votes
        }
        for result in results
    ]

    return media