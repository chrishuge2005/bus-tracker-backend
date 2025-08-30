from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory bus data
buses = {
    "1": {"lat": 12.9716, "lon": 77.5946, "name": "Campus Shuttle A", "status": "on-time", "lastUpdate": datetime.now().isoformat()},
    "2": {"lat": 12.9352, "lon": 77.6245, "name": "North Route", "status": "delayed", "lastUpdate": datetime.now().isoformat()},
    "3": {"lat": 12.9876, "lon": 77.5512, "name": "South Route", "status": "arriving", "lastUpdate": datetime.now().isoformat()}
}

@app.route('/buses', methods=['GET'])
def get_buses():
    return jsonify(buses)

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    bus_id = data.get('bus_id')
    lat = data.get('lat')
    lon = data.get('lon')

    if bus_id in buses:
        buses[bus_id]['lat'] = lat
        buses[bus_id]['lon'] = lon
        buses[bus_id]['lastUpdate'] = datetime.now().isoformat()
        return jsonify({"status": "success", "message": "Location updated"})
    else:
        return jsonify({"status": "error", "message": "Bus not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    
#     <!-- venv/Scripts/activate -->
#  <!-- uvicorn main:app --reload --host 0.0.0.0 --port 8000 -->