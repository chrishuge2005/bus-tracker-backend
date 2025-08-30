from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory bus data
buses = {
    "1": {"lat": 12.9716, "lon": 77.5946, "name": "Campus Shuttle A", "status": "on-time", "lastUpdate": datetime.now().isoformat(), "driver": None},
    "2": {"lat": 12.9352, "lon": 77.6245, "name": "North Route", "status": "delayed", "lastUpdate": datetime.now().isoformat(), "driver": None},
    "3": {"lat": 12.9876, "lon": 77.5512, "name": "South Route", "status": "arriving", "lastUpdate": datetime.now().isoformat(), "driver": None}
}

# Simple in-memory users
drivers = {
    "driver1": "password1",
    "driver2": "password2"
}

users = {
    "student1": "pass1",
    "staff1": "pass2"
}

# ================== Routes ==================

@app.route('/buses', methods=['GET'])
def get_buses():
    return jsonify(buses)

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    bus_id = data.get('bus_id')
    lat = data.get('lat')
    lon = data.get('lon')
    driver_id = data.get('driver_id')  # optional

    if bus_id in buses:
        buses[bus_id]['lat'] = lat
        buses[bus_id]['lon'] = lon
        buses[bus_id]['lastUpdate'] = datetime.now().isoformat()
        if driver_id:
            buses[bus_id]['driver'] = driver_id
        return jsonify({"status": "success", "message": "Location updated", "bus": buses[bus_id]})
    else:
        return jsonify({"status": "error", "message": "Bus not found"}), 404

@app.route('/login_driver', methods=['POST'])
def login_driver():
    data = request.json
    driver_id = data.get('driver_id')
    password = data.get('password')

    if driver_id in drivers and drivers[driver_id] == password:
        return jsonify({"status": "success", "message": "Driver login successful"})
    else:
        return jsonify({"status": "error", "message": "Invalid driver credentials"}), 401

@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    if user_id in users and users[user_id] == password:
        return jsonify({"status": "success", "message": "User login successful"})
    else:
        return jsonify({"status": "error", "message": "Invalid user credentials"}), 401

# ================== Run Server ==================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

#     <!-- venv/Scripts/activate -->
#  <!-- uvicorn main:app --reload --host 0.0.0.0 --port 8000 -->