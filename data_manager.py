import requests
from dotenv import  load_dotenv
import  os
load_dotenv()
from pprint import pprint
class DataManager:
     def __init__(self):
        self.destination_data={}

     def get_destination(self):
         response=requests.get(url=os.getenv('sheety_endpoint'))
         data=response.json()
         self.destination_data=data["prices"]
         # pprint(data["prices"])
         return self.destination_data


     def update_destination_codes(self):
         for city in self.destination_data:
             new_data = {
                 "price": {
                     "iataCode": city["iataCode"]
                 }
             }
             response = requests.put(
                 url=f"{sheety_endpoint}/{city['id']}",
                 json=new_data
             )
             print(response.text)



