[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

## Dataset Normalization and API Creation Project

This project focuses on normalizing a dataset of Movies & Shows, setting up a relational database, and creating an API for data reading and writing. It involves various data processing steps, including normalization, transformation, insertion into the database, and API creation for efficient data management.

### Key Features:

1. **Data Extraction and Normalization:** The dataset is sourced from Kaggle and undergoes preparation and normalization procedures to ensure consistency and reliability.
2. **Database Schema Definition:** SQLAlchemy is utilized to define the database schema, including tables for movies, shows, genres, ratings, and other relevant data.
3. **Data Insertion and Error Handling:** Data is inserted into the database tables, with error handling mechanisms implemented to log any SQLAlchemy errors encountered during insertion.
4. **API Creation:** Provides endpoints for reading from and writing to the database.
5. **Demo Recommender Engine:** Demonstrates reading and writing data using the API.

### Installation

Follow these steps to initialize and run this Poetry-based project in a new environment.

1. Clone this repository from your version control system (e.g., GitHub, GitLab).

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. Ensure that Poetry is installed in your new environment. If not, you can install it using the official installation script:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Navigate to the project directory and install the dependencies specified in the `pyproject.toml` file using Poetry:

    ```bash
    cd <project_directory>
    poetry install
    ```

    This command will create a virtual environment (if it doesn't already exist) and install all the dependencies listed in `pyproject.toml` and `poetry.lock`.

4. Poetry automatically manages virtual environments for you. To activate the virtual environment, you can use:

    ```bash
    poetry shell
    ```

    This will activate the environment, and you can start working within it.

5. Any project-specific commands or scripts can be run within this environment. The code utilizes the `decouple` library for defining environment variables. You can specify your `CONNECTION_STRING` and `BASE_URL` constants in your configuration file (such as a `.env` or `.ini` file) or modify them in the initialization code (check `env_example.txt` file).

6. You can download the dataset using `data_from_kaggle.py` by running:

    ```bash
    cd ./utils
    python data_from_kaggle.py
    ```

7. You can start the data extraction, normalization, and insertion process by running the following code:

    ```bash
    cd ./data_preparation
    python etl_pipeline.py
    ```

    **Alternatively:** For a guided data extraction and normalization procedure of the Movies & Shows dataset, refer to the `dataset_preparation_example.ipynb` Jupyter Notebook file (in the examples folder), which contains the full code.

8. Now that we have our database and schemas created, we can launch the server and run our API:

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 4 --log-level debug
    ```

    In this example:
    - `main:app` refers to the application instance.
    - `--host 0.0.0.0` makes the server accessible from any IP address.
    - `--port 8000` changes the port to `8000`.
    - `--reload` enables auto-reload.
    - `--workers 4` sets the number of worker processes to 4.
    - `--log-level debug` sets the log level to `debug`.

9. By default settings, we can access our API using a web browser via the link [http://127.0.0.1:8000](http://127.0.0.1:8000). By opening this link, you will enter the root page of the API. You can follow the provided links to access endpoints or use Swagger/Redoc documentation.

10. To use the demo recommender engine and see how it can read/write data using the API, run it by launching the following code:

    ```bash
    cd ./api
    python demo_recommender.py
    ```

### Suggestions for Future Improvements

- **Error Handling:** Some parts of the code currently don't handle potential errors explicitly. Consider implementing try-except blocks or custom error classes to handle issues like database connection failures, invalid CSV data format, or unexpected SQL exceptions.
- **Further Dataset Cleaning:** There might still be mistakes in the transformed dataset. Additional checks could be performed to ensure data integrity and correctness.
- **API Endpoint Creation:** More functionality could be achieved by creating additional endpoints for our API.

**Feel free to fork this repository and make your own modifications!**
