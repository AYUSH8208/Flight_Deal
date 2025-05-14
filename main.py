from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

notification_manager = NotificationManager()
data_manager = DataManager()
flight_search = FlightSearch()  # Ensure flight_search is always initialized
sheet_data = data_manager.get_destination()

if not sheet_data:
    print("No data available. Using mock data for the website.")
    sheet_data = [
        {"city": "Paris", "iataCode": "CDG", "lowestPrice": 100},
        {"city": "New York", "iataCode": "JFK", "lowestPrice": 300},
        {"city": "Tokyo", "iataCode": "HND", "lowestPrice": 500},
    ]

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet :\n {sheet_data}")
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_now = datetime.now() + timedelta(days=(6 * 30))

for locations in sheet_data:
    flight = flight_search.flight_search(
        origin_city_code="LON",
        destination_city_code=locations["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_now
    )
    if flight and flight.price < locations["lowestPrice"]:
        notification_manager.send_message(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )