import requests
from flight_data import FlightData
import os

class FlightSearch:
    def __init__(self):
        # API keys are loaded from environment variables, not hardcoded.
        self.kiwi_api_key = os.getenv('KIWI_API_KEY')
        self.kiwi_location_url = os.getenv('KIWI_LOCATION_URL')
        self.kiwi_search_url = os.getenv('KIWI_SEARCH_URL')

    def get_destination_code(self, city_name):
        location_url = f"{self.kiwi_location_url}/locations/query"
        headers = {"apikey": self.kiwi_api_key}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_url, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def flight_search(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": self.kiwi_api_key}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(
            url=f"{self.kiwi_search_url}/v2/search",
            headers=headers,
            params=query,
        )
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data


