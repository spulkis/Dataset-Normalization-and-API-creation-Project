from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MovieBase(BaseModel):
    """
    Base model for Movie objects.

    Attributes:
    - movie_id (str): Unique identifier for the movie.
    - title (str): Title of the movie.
    - release_year (int): Year of release of the movie.
    - age_certification (str, optional): Age certification of the movie.
    - runtime (int): Duration of the movie in minutes.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    movie_id: str
    title: str
    release_year: int
    age_certification: Optional[str]
    runtime: int

    class Config:
        from_attributes = True

class MovieActors(MovieBase):
    """
    Model for Movie objects including actors.

    Inherits:
    - MovieBase: Base model for Movie objects.

    Additional Attributes:
    - actor (str, optional): Name of an actor associated with the movie.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    actor: Optional[str]

    class Config:
        from_attributes = True

class MovieRating(MovieBase):
    """
    Model for Movie objects including rating details.

    Inherits:
    - MovieBase: Base model for Movie objects.

    Additional Attributes:
    - genre (str, optional): Genre of the movie.
    - imdb_score (float, optional): IMDB score of the movie.
    - imdb_votes (int, optional): Number of IMDB votes for the movie.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    genre: Optional[str]
    imdb_score: Optional[float]
    imdb_votes: Optional[int]

    class Config:
        from_attributes = True

class ShowBase(BaseModel):
    """
    Base model for Show objects.

    Attributes:
    - show_id (str): Unique identifier for the show.
    - title (str): Title of the show.
    - release_year (int): Year of release of the show.
    - age_certification (str, optional): Age certification of the show.
    - runtime (int): Duration of each episode of the show in minutes.
    - seasons (int): Number of seasons of the show.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    show_id: str
    title: str
    release_year: int
    age_certification: Optional[str]
    runtime: int
    seasons: int

    class Config:
        from_attributes = True

class ShowGenres(ShowBase):
    """
    Model for Show objects including genre.

    Inherits:
    - ShowBase: Base model for Show objects.

    Additional Attributes:
    - genre (str, optional): Genre of the show.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    genre: Optional[str]

    class Config:
        from_attributes = True

class MovieShow(BaseModel):
    """
    Represents a movie or show with detailed attributes.

    Attributes:
    - media_type (str): Type of media ('movie' or 'show').
    - movie_id (str, optional): Unique identifier for movies.
    - show_id (str, optional): Unique identifier for shows.
    - title (str, optional): Title of the movie or show.
    - release_year (int, optional): Year of release.
    - age_certification (str, optional): Age certification of the media.
    - runtime (int, optional): Duration of the movie or show in minutes.
    - genre (str, optional): Genre of the movie or show.
    - country (str, optional): Country of origin.
    - director (str, optional): Director of the movie or show.
    - actor (str, optional): Lead actor or actress in the movie or show.
    - character (str, optional): Character name in the movie or show.
    - imdb_score (float, optional): IMDb score of the movie or show.
    - imdb_votes (int, optional): Number of IMDb votes for the movie or show.

    Config:
    - from_attributes (bool): Enables attribute-based instantiation from dictionaries.
    """
    
    media_type: str
    movie_id: Optional[str]
    show_id: Optional[str]
    title: Optional[str]
    release_year: Optional[int]
    age_certification: Optional[str]
    runtime: Optional[int]
    genre: Optional[str]
    country: Optional[str]
    director: Optional[str]
    actor: Optional[str]
    character: Optional[str]
    imdb_score: Optional[float]
    imdb_votes: Optional[int]

    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    """
    Base model for Prediction objects.

    Attributes:
    - prediction_value (float): Value of the prediction.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    user_id: str
    prediction_value: float

class PredictionAdd(PredictionBase):
    """
    Model for adding a new Prediction object.

    Inherits:
    - PredictionBase: Base model for Prediction objects.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    pass

class PredictionResponse(PredictionBase):
    """
    Model for fetching Prediction objects with additional metadata.

    Inherits:
    - PredictionBase: Base model for Prediction objects.

    Additional Attributes:
    - index (int): Index of the prediction.
    - timestamp (datetime): Timestamp when the prediction was made.

    Config:
    - from_attributes (bool): Enables attribute based instantiation.
    """
    index: int
    timestamp: datetime
