import os
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

# Specify the dataset you want to download
dataset = 'thedevastator/the-ultimate-netflix-tv-shows-and-movies-dataset'

# Create a directory to store the dataset
os.makedirs('../datasets', exist_ok=True)

# Download and unzip the dataset
api.dataset_download_files(dataset, path='../datasets', unzip=True)