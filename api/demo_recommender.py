import requests
from typing import List
from decouple import config

class RecommenderEngine:
    def __init__(self, base_url: str):
        """
        Initialize the RecommenderEngine with a base URL.

        Args:
            base_url (str): The base URL of the API.
        """
        self.base_url = base_url.rstrip('/')

    def submit_prediction(self, user_id: str, prediction_value: float):
        """
        Submit a prediction to the API.

        Args:
            user_id (str): The user id to submit.
            prediction_value (float): The prediction value to submit.

        Returns:
            dict or None: The JSON response from the API if successful, None otherwise.
        """
        url = f"{self.base_url}/submit_prediction/"
        payload = {"user_id": user_id, "prediction_value": prediction_value}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to submit prediction: {response.status_code} - {response.text}")
            return None

    def get_predictions(self) -> List[float]:
        """
        Fetch predictions from the API.

        Returns:
            list: A list of prediction values fetched from the API.
        """
        url = f"{self.base_url}/get_predictions/"
        response = requests.get(url)
        if response.status_code == 200:
            predictions = response.json()
            return [{'index': prediction['index'], 'timestamp': prediction['timestamp'], 'user_id': prediction['user_id'], 'prediction_value': prediction['prediction_value']} for prediction in predictions]
        else:
            print(f"Failed to fetch predictions: {response.status_code} - {response.text}")
            return []

if __name__ == "__main__":
    # Load base URL from environment variables using python-decouple
    base_url = config('BASE_URL')

    # Initialize the RecommenderEngine with the base URL
    recommender = RecommenderEngine(base_url)

    # Example: Submitting a prediction
    while True:
        try:
            new_user_id = str(input("Insert your user ID: "))
            new_prediction_value = float(input("Insert prediction value: "))
            break  # Exit the loop if input is valid
        except ValueError:
            print("Invalid input, please enter a valid number.")

    new_prediction = recommender.submit_prediction(new_user_id, new_prediction_value)
    if new_prediction:
        print(f"Submitted prediction: {new_prediction}")

    # Example: Fetching predictions
    predictions = recommender.get_predictions()
    print(f"Fetched predictions: {predictions}")
