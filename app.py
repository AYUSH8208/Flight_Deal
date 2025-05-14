from flask import Flask, render_template, request, jsonify
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

app = Flask(__name__)

# Initialize backend components
notification_manager = NotificationManager()
data_manager = DataManager()
flight_search = FlightSearch()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update-destination-codes', methods=['POST'])
def update_destination_codes():
    sheet_data = data_manager.get_destination()
    for row in sheet_data:
        if not row["iataCode"]:
            row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()
    return jsonify({"status": "success", "message": "Destination codes updated!"})

@app.route('/search-flights', methods=['POST'])
def search_flights():
    origin_city_code = request.form.get('origin_city_code', '').strip()
    destination_city = request.form.get('destination_city', '').strip()
    from_time = request.form.get('from_time', '').strip()
    to_time = request.form.get('to_time', '').strip()

    # Input validation
    if not origin_city_code or not destination_city or not from_time or not to_time:
        return jsonify({"status": "error", "message": "All fields are required."})

    try:
        from_time = datetime.strptime(from_time, '%Y-%m-%d')
        to_time = datetime.strptime(to_time, '%Y-%m-%d')
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format. Use YYYY-MM-DD."})

    if from_time >= to_time:
        return jsonify({"status": "error", "message": "From date must be earlier than To date."})

    destination_code = flight_search.get_destination_code(destination_city)
    if not destination_code:
        return jsonify({"status": "error", "message": f"Invalid destination city: {destination_city}"})

    flight = flight_search.flight_search(
        origin_city_code=origin_city_code,
        destination_city_code=destination_code,
        from_time=from_time,
        to_time=to_time
    )

    if flight:
        return jsonify({
            "status": "success",
            "flight": {
                "price": flight.price,
                "origin_city": flight.origin_city,
                "origin_airport": flight.origin_airport,
                "destination_city": flight.destination_city,
                "destination_airport": flight.destination_airport,
                "out_date": flight.out_date,
                "return_date": flight.return_date
            }
        })
    else:
        return jsonify({"status": "error", "message": "No flights found."})

if __name__ == '__main__':
    app.run(debug=True)
