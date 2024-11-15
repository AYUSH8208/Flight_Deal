from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime,timedelta
from notification_manager import NotificationManager
notification_manager=NotificationManager()
data_manager=DataManager()
sheet_data=data_manager.get_destination()
flight_search=FlightSearch()

if sheet_data[0]["iataCode"] =="":
    from flight_search import FlightSearch
    flight_search=FlightSearch()

    for row in sheet_data:
        row["iataCode"]= flight_search.get_destination_code(row["city"])
    print(f"sheet :\n {sheet_data}")
    data_manager.destination_data=sheet_data
    data_manager.update_destination_codes()

tomorrow=datetime.now() + timedelta(days=1)
six_months_from_now=datetime.now()+ timedelta(days=(6*30))

for locations in sheet_data:
    flight=flight_search.flight_search(origin_city_code="LON",destination_city_code=locations["iataCode"],from_time=tomorrow,to_time=six_months_from_now)
    if flight.price < locations["lowestPrice"]:
        notification_manager.send_message(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )