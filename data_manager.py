import requests
from dotenv import load_dotenv
import os

load_dotenv()

from pprint import pprint

class DataManager:
    def __init__(self):
        self.destination_data = []
        self.sheety_api_key = os.getenv('SHEETY_API_KEY')
        self.sheety_endpoint = os.getenv('SHEETY_ENDPOINT')

    def get_destination(self):
        try:
            headers = {
                "Authorization": f"Bearer {self.sheety_api_key}"
            }
            response = requests.get(
                self.sheety_endpoint,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            # Check if "prices" key exists
            if "prices" not in data:
                raise KeyError("The key 'prices' is missing in the response data.")

            self.destination_data = data["prices"]
            return self.destination_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from the endpoint: {e}")
            return []
        except KeyError as e:
            print(f"Error in data structure: {e}")
            return []

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.sheety_endpoint}/{city['id']}",
                json=new_data,
                headers={"Authorization": f"Bearer {self.sheety_api_key}"}
            )
            print(response.text)



