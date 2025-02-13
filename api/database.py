from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database 
from decouple import config

# Load environment variables
CONNECTION_STRING = config('CONNECTION_STRING')

# Create a database engine
engine = create_engine(CONNECTION_STRING)

# Create a declarative base
Base = declarative_base()

# Create a sessionmaker with bound engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)