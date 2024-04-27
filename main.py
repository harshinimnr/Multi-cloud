from flask import Flask, render_template, request, jsonify
import requests
import json
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def get_directions(api_key, origin, destination, mode):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "key": api_key,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


@app.route('/find_best_transportation', methods=['GET'])
def find_best_transportation_api():
    from_city = request.args.get('from_city', '')
    to_city = request.args.get('to_city', '')

    # Google Maps API key
    api_key = "GOOGLE_MAPS_API_KEY"

    # Define the origin and destination cities
    origin = from_city + ", Indiana"
    destination = to_city + ", Indiana"

    # List of transportation modes
    transportation_modes = ["driving", "transit", "walking", "bicycling"]

    results = []
    for mode in transportation_modes:
        try:
            data = get_directions(api_key, origin, destination, mode)

            # Parse the response to extract information
            if data.get("status") == "OK":
                route = data["routes"][0]
                leg = route["legs"][0]
                distance = leg["distance"]["text"]
                duration = leg["duration"]["text"]
                steps = leg["steps"]

                result = {
                    "from_city": from_city,
                    "to_city": to_city,
                    "mode": mode,
                    "distance": distance,
                    "duration": duration,
                    "directions": [step["html_instructions"] for step in steps],
                }

                results.append(result)
            else:
                results.append({"error": f"Unable to find transportation information for mode: {mode}"})
        except Exception as e:
            results.append({"error": f"Error for mode {mode}: {str(e)}"})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
