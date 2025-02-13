from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse
from . import crud, models, schemas  # Importing local modules
from .database import SessionLocal, engine  # Importing database session and engine
from sqlalchemy.orm import Session
import json

# Custom JSONResponse class to pretty-print JSON responses
class PrettyJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(content, indent=4, ensure_ascii=False).encode("utf-8")

# Creating FastAPI instance
app = FastAPI(default_response_class=PrettyJSONResponse)

# Creating database tables
models.Base.metadata.create_all(bind=engine)

# Dependency function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint returning HTML response with API information
@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Returns HTML content with links to available API endpoints.
    """
    html_content = """
    <html>
        <head>
            <title>Movies and Shows Database API</title>
        </head>
        <body>
            <h1>Welcome to the Movies and Shows Database API</h1>
            <p>Version: 0.1.1</p>
            <p>Available Endpoints:</p>
            <ul>
                <li><a href="/movies/">Get Movies</a></li>
                <li><a href="/movies/movies_by_actor/?actor_name=Nicolas%20Cage">Get Movies by Actor (e.g. - 'Nicolas Cage')</a></li>
                <li><a href="/movies/movies_by_ratings/">Get Movies best rated on IMDB</a></li>
                <li><a href="/shows/">Get Shows</a></li>
                <li><a href="/shows/shows_by_details/">Get Shows By Details</a></li>
                <li><a href="/media_details/">Get All Available Media</a></li>
                <li><a href="/submit_predictions/">Post predictions</a></li>
                <li><a href="/get_predictions/">Get predictions</a></li>
                <li><a href="/docs">Swagger UI Documentation</a></li>
                <li><a href="/redoc">Redoc Documentation</a></li>
            </ul>
            <p>Author: Julius</p>
        </body>
    </html>
    """
    return html_content

# Endpoint to fetch movies with optional pagination
@app.get("/movies/", response_model=List[schemas.MovieBase])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetches a list of movies with optional pagination.

    Parameters:
    - skip (int): Number of records to skip.
    - limit (int): Maximum number of records to fetch.
    - db (Session): Database session dependency.

    Returns:
    - List[schemas.MovieBase]: List of movie records.
    """
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

# Endpoint to fetch movies by actor name
@app.get("/movies/movies_by_actor/", response_model=List[schemas.MovieActors])
def read_movies_by_actor(
    actor_name: str, db: Session = Depends(get_db)
):
    """
    Fetches a list of movies featuring a specific actor.

    Parameters:
    - actor_name (str): Name of the actor.
    - db (Session): Database session dependency.

    Returns:
    - List[schemas.MovieActors]: List of movie records with actor information.
    """
    movies = crud.get_movies_by_actors(db, actor_name)
    return movies

# Endpoint to fetch movies by ratings criteria
@app.get("/movies/movie_by_rating/", response_model=List[schemas.MovieRating])
def read_movie_by_rating(
    release_year: Optional[int] = Query(None, ge=1888, le=2100),
    genre: Optional[str] = Query(None, min_length=1, max_length=20),
    db: Session = Depends(get_db)
):
    """
    Fetches a movie that is rated best on IMDB site.

    Parameters:
    - release_year (int, optional): Release year of the movie.
    - genre (str, optional): Genre of the movie.
    - db (Session): Database session dependency.

    Returns:
    - List[schemas.MovieRating]: List of movie records with rating information.
    """
    movies = crud.get_movie_by_ratings(db, release_year=release_year, genre=genre)
    return movies

# Endpoint to fetch shows with optional pagination
@app.get("/shows/", response_model=List[schemas.ShowBase])
def read_shows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetches a list of shows with optional pagination.

    Parameters:
    - skip (int): Number of records to skip.
    - limit (int): Maximum number of records to fetch.
    - db (Session): Database session dependency.

    Returns:
    - List[schemas.ShowBase]: List of show records.
    """
    shows = crud.get_shows(db, skip=skip, limit=limit)
    return shows

# Endpoint to fetch shows by detailed criteria
@app.get("/shows/shows_by_details/", response_model=List[schemas.ShowGenres])
def read_shows_by_details(
    title: Optional[str] = Query(None, min_length=3, max_length=50),
    release_year: Optional[int] = Query(None, ge=1888, le=2100),
    age_certification: Optional[str] = Query(None, min_length=1, max_length=10),
    genre: Optional[str] = Query(None, min_length=1, max_length=20),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Fetches a list of shows based on detailed search criteria.

    Parameters:
    - title (str, optional): Title of the show.
    - release_year (int, optional): Release year of the show.
    - age_certification (str, optional): Age certification of the show.
    - genre (str, optional): Genre of the show.
    - skip (int): Number of records to skip.
    - limit (int): Maximum number of records to fetch.
    - db (Session): Database session dependency.

    Returns:
    - List[schemas.ShowGenres]: List of show records with genre information.
    """
    shows = crud.get_shows_by_details(db, title=title, release_year=release_year, 
                                      age_certification=age_certification, genre=genre, 
                                      skip=skip, limit=limit)
    return shows

# Endpoint to fetch movies and shows by detailed criteria
@app.get("/media_details/", response_model=List[schemas.MovieShow])
def read_media(
    media_type: Optional[str] = Query(None, min_length=1, max_length=10),
    title: Optional[str] = Query(None, min_length=3, max_length=50),
    release_year: Optional[int] = Query(None, ge=1888, le=2100),
    age_certification: Optional[str] = Query(None, min_length=1, max_length=10),
    genre: Optional[str] = Query(None, min_length=1, max_length=20),
    country: Optional[str] = Query(None, min_length=1, max_length=10),
    director: Optional[str] = Query(None, min_length=1, max_length=50),
    actor: Optional[str] = Query(None, min_length=1, max_length=50),
    character: Optional[str] = Query(None, min_length=1, max_length=50),
    imdb_score: Optional[float] = Query(None),
    imdb_votes: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Fetches movies and shows based on detailed criteria.

    Parameters:
    - media_type (str, optional): Type of media (e.g., 'movie', 'show').
    - title (str, optional): Title of the movie or show.
    - release_year (int, optional): Year of release.
    - age_certification (str, optional): Age certification of the media.
    - genre (str, optional): Genre of the media.
    - country (str, optional): Country of origin.
    - director (str, optional): Director of the media.
    - actor (str, optional): Actor in the media.
    - character (str, optional): Character name in the media.
    - imdb_score (float, optional): IMDb score of the media (lists media rated greater than given value).
    - imdb_votes (int, optional): Number of IMDb votes (lists media that have more votes than given value).
    - skip (int, optional): Number of records to skip for pagination.
    - limit (int, optional): Maximum number of records to fetch.

    Returns:
    - List[schemas.MovieShow]: List of movies and shows matching the criteria.
    """
    media = crud.get_media(db, media_type=media_type, title=title, release_year=release_year, 
                                      age_certification=age_certification, genre=genre,
                                      country=country, director=director,
                                      actor=actor, character=character, imdb_score=imdb_score, imdb_votes=imdb_votes,
                                      skip=skip, limit=limit)
    return media

# Endpoint to submit a prediction
@app.post("/submit_prediction/", response_model=schemas.PredictionAdd)
def submit_prediction(prediction: schemas.PredictionAdd, db: Session = Depends(get_db)):
    """
    Creates a new prediction record in the database.

    Parameters:
    - prediction (schemas.PredictionAdd): Prediction data to be created.
    - db (Session): Database session dependency.

    Returns:
    - schemas.PredictionAdd: Created prediction record.
    """
    db_prediction = models.Predictions(user_id=prediction.user_id, prediction_value=prediction.prediction_value)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

# Endpoint to fetch all predictions
@app.get("/get_predictions/", response_model=List[schemas.PredictionResponse])
def get_predictions(db: Session = Depends(get_db)):
    """
    Fetches all predictions stored in the database.

    Parameters:
    - db (Session): Database session dependency.

    Returns:
    - List[schemas.PredictionResponse]: List of prediction records.
    """
    predictions = db.query(models.Predictions).all()
    return predictions
