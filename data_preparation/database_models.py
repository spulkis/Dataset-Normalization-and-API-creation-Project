from sqlalchemy import ForeignKeyConstraint, Column, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone, timedelta

Base = declarative_base()
Base_view = declarative_base()

class Movies(Base):
    """
    Represents the movies table in the database.

    Attributes:
        index (int): Primary key for the movies table.
        movie_id (str): Unique identifier for the movie.
        title (str): Title of the movie.
        release_year (int): Year the movie was released.
        age_certification (str): Age certification for the movie.
        runtime (int): Runtime of the movie in minutes.
    """
    __tablename__ = "movies"

    index = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    movie_id = Column(String(128), index=True)
    title = Column(String(512))
    release_year = Column(Integer)
    age_certification = Column(String(512))
    runtime = Column(Integer)

    def __init__(self, movie_id, title, release_year, age_certification, runtime):
        """
        Initializes a Movies instance.

        Args:
            movie_id (str): Unique identifier for the movie.
            title (str): Title of the movie.
            release_year (int): Year the movie was released.
            age_certification (str): Age certification for the movie.
            runtime (int): Runtime of the movie in minutes.
        """
        self.movie_id = movie_id
        self.title = title
        self.release_year = release_year 
        self.age_certification = age_certification
        self.runtime = runtime

    def __repr__(self):
        """
        Provides a string representation of the Movies instance.

        Returns:
            str: String representation of the Movies instance.
        """
        return (
        f"<Movies(movie_id={self.movie_id}, title={self.title}, release_year={self.release_year}, "
        f"age_certification={self.age_certification}, runtime={self.runtime})>"
        )

class Shows(Base):
    """
    Represents the shows table in the database.

    Attributes:
        index (int): Primary key for the shows table.
        show_id (str): Unique identifier for the show.
        title (str): Title of the show.
        release_year (int): Year the show was released.
        age_certification (str): Age certification for the show.
        runtime (int): Runtime of the show in minutes.
        seasons (int): Number of seasons of the show.
    """
    __tablename__ = "shows"

    index = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    show_id = Column(String(128), index=True)
    title = Column(String(512))
    release_year = Column(Integer)
    age_certification = Column(String(512))
    runtime = Column(Integer)
    seasons = Column(Integer)

    def __init__(self, show_id, title, release_year, age_certification, runtime, seasons):
        """
        Initializes a Shows instance.

        Args:
            show_id (str): Unique identifier for the show.
            title (str): Title of the show.
            release_year (int): Year the show was released.
            age_certification (str): Age certification for the show.
            runtime (int): Runtime of the show in minutes.
            seasons (int): Number of seasons of the show.
        """
        self.show_id = show_id
        self.title = title
        self.release_year = release_year 
        self.age_certification = age_certification
        self.runtime = runtime
        self.seasons = seasons

    def __repr__(self):
        """
        Provides a string representation of the Shows instance.

        Returns:
            str: String representation of the Shows instance.
        """
        return (
        f"<Shows(show_id={self.show_id}, title={self.title}, release_year={self.release_year}, "
        f"age_certification={self.age_certification}, runtime={self.runtime}, seasons={self.seasons})>"
        )

class Genres(Base):
    """
    Represents the genres table in the database.

    Attributes:
        genre_id (int): Primary key for the genres table.
        genre (str): Genre name.
    """
    __tablename__ = "genres"
    
    genre_id = Column(Integer, primary_key=True, unique=True, index=True)
    genre = Column(String(255))

    def __init__(self, genre_id, genre):
        """
        Initializes a Genres instance.

        Args:
            genre_id (int): Primary key for the genres table.
            genre (str): Genre name.
        """
        self.genre_id = genre_id
        self.genre = genre

    def __repr__(self):
        """
        Provides a string representation of the Genres instance.

        Returns:
            str: String representation of the Genres instance.
        """
        return f"<Genres(genre_id={self.genre_id}, genre={self.genre})>"

class GenresBridge(Base):
    """
    Represents the genres_bridge table in the database.

    Attributes:
        index (int): Primary key for the genres_bridge table.
        movie_id (str): Unique identifier for the movie.
        show_id (str): Unique identifier for the show.
        genre_id (int): Foreign key for the genres table.
    """
    __tablename__ = "genres_bridge"
    # Define conditional relationships
    movie = relationship("Movies", primaryjoin="GenresBridge.movie_id == Movies.movie_id", uselist=False)
    show = relationship("Shows", primaryjoin="GenresBridge.show_id == Shows.show_id", uselist=False)
    genre = relationship("Genres", primaryjoin="GenresBridge.genre_id == Genres.genre_id", uselist=False)
    __table_args__ = (
        ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], name='fk_g_movie_id'),
        ForeignKeyConstraint(['show_id'], ['shows.show_id'], name='fk_g_show_id'),
        ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], name='fk_genre_id')
    )
    index = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(128))
    show_id = Column(String(128))
    genre_id = Column(Integer, nullable=False)

    def __init__(self, movie_id, show_id, genre_id):
        """
        Initializes a GenresBridge instance.

        Args:
            movie_id (str): Unique identifier for the movie.
            show_id (str): Unique identifier for the show.
            genre_id (int): Foreign key for the genres table.
        """
        self.movie_id = movie_id
        self.show_id = show_id
        self.genre_id = genre_id

    def __repr__(self):
        """
        Provides a string representation of the GenresBridge instance.

        Returns:
            str: String representation of the GenresBridge instance.
        """
        return f"<GenresBridge(movie_id={self.movie_id}, show_id={self.show_id}, genre_id={self.genre_id})>"

class ProductionCountries(Base):
    """
    Represents the production_countries table in the database.

    Attributes:
        country_id (int): Primary key for the production_countries table.
        country (str): Name of the production country.
    """
    __tablename__ = "production_countries"
    
    country_id = Column(Integer, primary_key=True, unique=True, index=True)
    country = Column(String(255))

    def __init__(self, country_id, country):
        """
        Initializes a ProductionCountries instance.

        Args:
            country_id (int): Primary key for the production_countries table.
            country (str): Name of the production country.
        """
        self.country_id = country_id
        self.country = country

    def __repr__(self):
        """
        Provides a string representation of the ProductionCountries instance.

        Returns:
            str: String representation of the ProductionCountries instance.
        """
        return f"<Countries(country_id={self.country_id}, country={self.country})>"

class ProductionCountriesBridge(Base):
    """
    Represents the production_countries_bridge table in the database.

    Attributes:
        index (int): Primary key for the production_countries_bridge table.
        movie_id (str): Unique identifier for the movie.
        show_id (str): Unique identifier for the show.
        country_id (int): Foreign key for the production_countries table.
    """
    __tablename__ = "production_countries_bridge"
    # Define conditional relationships
    movie = relationship("Movies", primaryjoin="ProductionCountriesBridge.movie_id == Movies.movie_id", uselist=False)
    show = relationship("Shows", primaryjoin="ProductionCountriesBridge.show_id == Shows.show_id", uselist=False)
    production_country = relationship("ProductionCountries", primaryjoin="ProductionCountriesBridge.country_id == ProductionCountries.country_id", uselist=False)
    __table_args__ = (
        ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], name='fk_pc_movie_id'),
        ForeignKeyConstraint(['show_id'], ['shows.show_id'], name='fk_pc_show_id'),
        ForeignKeyConstraint(['country_id'], ['production_countries.country_id'], name='fk_country_id')
    )
    index = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(128))
    show_id = Column(String(128))
    country_id = Column(Integer, nullable=False)

    def __init__(self, movie_id, show_id, country_id):
        """
        Initializes a ProductionCountriesBridge instance.

        Args:
            movie_id (str): Unique identifier for the movie.
            show_id (str): Unique identifier for the show.
            country_id (int): Foreign key for the production_countries table.
        """
        self.movie_id = movie_id
        self.show_id = show_id
        self.country_id = country_id

    def __repr__(self):
        """
        Provides a string representation of the ProductionCountriesBridge instance.

        Returns:
            str: String representation of the ProductionCountriesBridge instance.
        """
        return f"<ProductionCountriesBridge(movie_id={self.movie_id}, show_id={self.show_id}, country_id={self.country_id})>"

class Actors(Base):
    """
    Represents the actors table in the database.

    Attributes:
        index (int): Primary key for the actors table.
        actor_id (int): Unique identifier for the actor.
        actor (str): Name of the actor.
    """
    __tablename__ = "actors"

    index = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    actor_id = Column(Integer, index=True)
    actor = Column(String(512))

    def __init__(self, actor_id, actor):
        """
        Initializes an Actors instance.

        Args:
            actor_id (int): Unique identifier for the actor.
            actor (str): Name of the actor.
        """
        self.actor_id = actor_id
        self.actor = actor

    def __repr__(self):
        """
        Provides a string representation of the Actors instance.

        Returns:
            str: String representation of the Actors instance.
        """
        return f"<Actors(actor_id={self.actor_id}, actor={self.actor})>"
    
class ActorsBridge(Base):
    """
    Represents the actors_bridge table in the database.

    Attributes:
        index (int): Primary key for the actors_bridge table.
        movie_id (str): Unique identifier for the movie.
        show_id (str): Unique identifier for the show.
        actor_id (int): Foreign key for the actors table.
    """
    __tablename__ = "actors_bridge"
    # Define conditional relationships
    movie = relationship("Movies", primaryjoin="ActorsBridge.movie_id == Movies.movie_id", uselist=False)
    show = relationship("Shows", primaryjoin="ActorsBridge.show_id == Shows.show_id", uselist=False)
    actor = relationship("ProductionCountries", primaryjoin="ActorsBridge.actor_id == Actors.actor_id", uselist=False)
    __table_args__ = (
        ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], name='fk_a_movie_id'),
        ForeignKeyConstraint(['show_id'], ['shows.show_id'], name='fk_a_show_id'),
        ForeignKeyConstraint(['actor_id'], ['actors.actor_id'], name='fk_actor_id')
    )
    index = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(128))
    show_id = Column(String(128))
    actor_id = Column(Integer, nullable=False)

    def __init__(self, movie_id, show_id, actor_id):
        """
        Initializes a ActorsBridge instance.

        Args:
            movie_id (str): Unique identifier for the movie.
            show_id (str): Unique identifier for the show.
            actor_id (int): Foreign key for the actors table.
        """
        self.movie_id = movie_id
        self.show_id = show_id
        self.actor_id = actor_id

    def __repr__(self):
        """
        Provides a string representation of the ActorsBridge instance.

        Returns:
            str: String representation of the ActorsBridge instance.
        """
        return f"<ActorsBridge(movie_id={self.movie_id}, show_id={self.show_id}, actor_id={self.actor_id})>"
    
class Directors(Base):
    """
    Represents the directors table in the database.

    Attributes:
        index (int): Primary key for the directors table.
        director_id (int): Unique identifier for the director.
        director (str): Name of the director.
    """
    __tablename__ = "directors"

    index = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    director_id = Column(Integer, index=True)
    director = Column(String(512))

    def __init__(self, director_id, director):
        """
        Initializes a Directors instance.

        Args:
            director_id (int): Unique identifier for the director.
            director (str): Name of the director.
        """
        self.director_id = director_id
        self.director = director

    def __repr__(self):
        """
        Provides a string representation of the Directors instance.

        Returns:
            str: String representation of the Directors instance.
        """
        return f"<Directors(director_id={self.director_id}, director={self.director})>"
    
class DirectorsBridge(Base):
    """
    Represents the directors_bridge table in the database.

    Attributes:
        index (int): Primary key for the directors_bridge table.
        movie_id (str): Unique identifier for the movie.
        show_id (str): Unique identifier for the show.
        director_id (int): Foreign key for the actors table.
    """
    __tablename__ = "directors_bridge"
    # Define conditional relationships
    movie = relationship("Movies", primaryjoin="DirectorsBridge.movie_id == Movies.movie_id", uselist=False)
    show = relationship("Shows", primaryjoin="DirectorsBridge.show_id == Shows.show_id", uselist=False)
    director = relationship("Directors", primaryjoin="DirectorsBridge.director_id == Directors.director_id", uselist=False)
    __table_args__ = (
        ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], name='fk_d_movie_id'),
        ForeignKeyConstraint(['show_id'], ['shows.show_id'], name='fk_d_show_id'),
        ForeignKeyConstraint(['director_id'], ['directors.director_id'], name='fk_director_id')
    )
    index = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(128))
    show_id = Column(String(128))
    director_id = Column(Integer, nullable=False)

    def __init__(self, movie_id, show_id, director_id):
        """
        Initializes a DirectorsBridge instance.

        Args:
            movie_id (str): Unique identifier for the movie.
            show_id (str): Unique identifier for the show.
            director_id (int): Foreign key for the actors table.
        """
        self.movie_id = movie_id
        self.show_id = show_id
        self.director_id = director_id

    def __repr__(self):
        """
        Provides a string representation of the DirectorsBridge instance.

        Returns:
            str: String representation of the DirectorsBridge instance.
        """
        return f"<DirectorsBridge(movie_id={self.movie_id}, show_id={self.show_id}, director_id={self.director_id})>"
    
class Characters(Base):
    """
    Represents the characters table in the database.

    Attributes:
        character_id (int): Primary key for the characters table.
        character (str): Name of the character.
    """
    __tablename__ = "characters"
    
    character_id = Column(Integer, primary_key=True, unique=True, index=True)
    character = Column(String(255))

    def __init__(self, character_id, character):
        """
        Initializes a Characters instance.

        Args:
            character_id (int): Primary key for the characters table.
            character (str): Name of the character.
        """
        self.character_id = character_id
        self.character = character

    def __repr__(self):
        """
        Provides a string representation of the Characters instance.

        Returns:
            str: String representation of the Characters instance.
        """
        return f"<Characters(character_id={self.character_id}, character={self.character})>"

class CharactersBridge(Base):
    """
    Represents the characters_bridge table in the database.

    Attributes:
        index (int): Primary key for the characters_bridge table.
        movie_id (str): Unique identifier for the movie.
        show_id (str): Unique identifier for the show.
        actor_id (int): Unique identifier for the actor.
        character_id (int): Foreign key for the characters table.
    """
    __tablename__ = "characters_bridge"
    # Define conditional relationships
    movie = relationship("Movies", primaryjoin="CharactersBridge.movie_id == Movies.movie_id", uselist=False)
    show = relationship("Shows", primaryjoin="CharactersBridge.show_id == Shows.show_id", uselist=False)
    actor = relationship('Actors', primaryjoin="CharactersBridge.actor_id == Actors.actor_id", uselist=False)
    character = relationship('Characters', primaryjoin="CharactersBridge.character_id == Characters.character_id", uselist=False)
    __table_args__ = (
        ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], name='fk_c_movie_id'),
        ForeignKeyConstraint(['show_id'], ['shows.show_id'], name='fk_c_show_id'),
        ForeignKeyConstraint(['actor_id'], ['actors.actor_id'], name='fk_c_actor_id'),
        ForeignKeyConstraint(['character_id'], ['characters.character_id'], name='fk_character_id')
    )
    index = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(String(128))
    show_id = Column(String(128))
    actor_id = Column(Integer)
    character_id = Column(Integer)

    def __init__(self, movie_id, show_id, actor_id, character_id):
        """
        Initializes a CharactersBridge instance.

        Args:
            movie_id (str): Unique identifier for the movie.
            show_id (str): Unique identifier for the show.
            actor_id (int): Unique identifier for the actor.
            character_id (int): Foreign key for the characters table.
        """
        self.movie_id = movie_id
        self.show_id = show_id
        self.actor_id = actor_id
        self.character_id = character_id

    def __repr__(self):
        """
        Provides a string representation of the CharactersBridge instance.

        Returns:
            str: String representation of the CharactersBridge instance.
        """
        return f"<CharactersBridge(movie_id={self.movie_id}, show_id={self.show_id}, actor_id={self.actor_id}, character_id={self.character_id})>"

class IMDBInfo(Base):
    """
    Represents the imdb_info table in the database.

    Attributes:
        index (int): Primary key for the imdb_info table.
        movie_id (str): Unique identifier for the movie.
        show_id (str): Unique identifier for the show.
        imdb_id (str): Unique identifier for the IMDB entry.
        imdb_score (float): IMDB score.
        imdb_votes (int): Number of votes on IMDB.
    """
    __tablename__ = "imdb_info"
    # Define conditional relationships
    movie = relationship("Movies", primaryjoin="IMDBInfo.movie_id == Movies.movie_id", uselist=False)
    show = relationship("Shows", primaryjoin="IMDBInfo.show_id == Shows.show_id", uselist=False)
    __table_args__ = (
        ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], name='fk_imdb_movie_id'),
        ForeignKeyConstraint(['show_id'], ['shows.show_id'], name='fk_imdb_show_id')
    )
    index = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    movie_id = Column(String(128))
    show_id = Column(String(128))
    imdb_id = Column(String(128))
    imdb_score = Column(Float)
    imdb_votes = Column(Integer)


    def __init__(self, movie_id, show_id, imdb_id, imdb_score, imdb_votes):
        """
        Initializes an IMDBInfo instance.

        Args:
            movie_id (str): Unique identifier for the movie.
            show_id (str): Unique identifier for the show.
            imdb_id (str): Unique identifier for the IMDB entry.
            imdb_score (float): IMDB score.
            imdb_votes (int): Number of votes on IMDB.
        """
        self.movie_id = movie_id
        self.show_id = show_id
        self.imdb_id = imdb_id
        self.imdb_score = imdb_score
        self.imdb_votes = imdb_votes

    def __repr__(self):
        """
        Provides a string representation of the IMDBInfo instance.

        Returns:
            str: String representation of the IMDBInfo instance.
        """
        return f"<IMDBInfo(movie_id={self.movie_id}, show_id={self.show_id}, imdb_id={self.imdb_id}, imdb_score={self.imdb_score}, imdb_votes={self.imdb_votes})>"

class Predictions(Base):
    """
    Represents a prediction record in the database.

    Attributes:
        index (int): Unique identifier for the prediction record (auto-incrementing integer).
        timestamp (datetime): Datetime when the prediction was made (automatically set to UTC on creation).
        prediction_value (float): The actual predicted value.
    """

    __tablename__ = "predictions"

    index = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=2))))
    user_id = Column(String(64), nullable=False)
    prediction_value = Column(Float, nullable=False)

    def __init__(self, user_id, prediction_value):
        """
        Initializes a new prediction object.

        Args:
            timestamp (datetime): The datetime when the prediction was made.
            prediction_value (float): The predicted value.
        """

        self.timestamp =  datetime.now(timezone(timedelta(hours=2)))
        self.user_id =  user_id
        self.prediction_value = prediction_value

    def __repr__(self):
        """
        Returns a string representation of the prediction object.

        Returns:
            str: A string representation of the prediction object in the format
                `<Predictions(timestamp=..., prediction_value=...)>`.
        """

        return f"<Predictions(timestamp={self.timestamp}, user_id={self.user_id}, prediction_value={self.prediction_value})>"
