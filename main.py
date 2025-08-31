from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory bus data
buses = {
    "1": {"lat": 12.9716, "lng": 77.5946, "name": "Campus Shuttle A", "status": "inactive", "lastUpdate": datetime.now().isoformat(), "driver": None},
    "2": {"lat": 12.9352, "lng": 77.6245, "name": "North Route", "status": "inactive", "lastUpdate": datetime.now().isoformat(), "driver": None},
    "3": {"lat": 12.9876, "lng": 77.5512, "name": "South Route", "status": "inactive", "lastUpdate": datetime.now().isoformat(), "driver": None},
    "4": {"lat": 12.9563, "lng": 77.5768, "name": "East Route", "status": "inactive", "lastUpdate": datetime.now().isoformat(), "driver": None}
}

# Simple in-memory users
drivers = {
    "driver1": {"password": "pass1", "busId": "1", "name": "John Smith"},
    "driver2": {"password": "pass2", "busId": "2", "name": "Maria Garcia"},
    "driver3": {"password": "pass3", "busId": "3", "name": "Robert Johnson"},
    "driver4": {"password": "pass4", "busId": "4", "name": "Sarah Wilson"}
}

students = {
    "student1": {"password": "pass1", "name": "Alex Johnson"},
    "student2": {"password": "pass2", "name": "Emma Davis"},
    "student3": {"password": "pass3", "name": "Michael Brown"}
}

# ================== Routes ==================

@app.route('/buses', methods=['GET'])
def get_buses():
    """Return all buses with latest location and status."""
    return jsonify(buses), 200

@app.route('/buses/<bus_id>/location', methods=['POST'])
def update_bus_location(bus_id):
    """
    Drivers send their current location to update the server.
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    lat = data.get('lat')
    lng = data.get('lng')
    timestamp = data.get('timestamp')
    
    if lat is None or lng is None:
        return jsonify({"status": "error", "message": "Latitude and longitude required"}), 400

    if bus_id in buses:
        buses[bus_id]['lat'] = lat
        buses[bus_id]['lng'] = lng
        buses[bus_id]['status'] = 'active'
        buses[bus_id]['lastUpdate'] = timestamp or datetime.now().isoformat()
        return jsonify({"status": "success", "message": "Location updated", "bus": buses[bus_id]}), 200
    else:
        return jsonify({"status": "error", "message": "Bus not found"}), 404

@app.route('/driver/login', methods=['POST'])
def login_driver():
    """Driver login: assign driver to their bus."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    driver_id = data.get('driver_id')
    password = data.get('password')
    bus_id = data.get('bus_id')

    if not driver_id or not password or not bus_id:
        return jsonify({"status": "error", "message": "Driver ID, password and bus ID required"}), 400

    if driver_id in drivers and drivers[driver_id]['password'] == password:
        # Check if driver is assigned to this bus
        if drivers[driver_id]['busId'] != bus_id:
            return jsonify({"status": "error", "message": "Driver not assigned to this bus"}), 403
            
        # Assign driver to bus and set status to active
        buses[bus_id]['driver'] = driver_id
        buses[bus_id]['status'] = 'active'
        return jsonify({
            "status": "success", 
            "message": "Driver login successful", 
            "busId": bus_id,
            "driverName": drivers[driver_id]['name']
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid driver credentials"}), 401

@app.route('/driver/logout', methods=['POST'])
def logout_driver():
    """Driver logout: release bus assignment."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    driver_id = data.get('driver_id')
    bus_id = data.get('bus_id')

    if not driver_id or not bus_id:
        return jsonify({"status": "error", "message": "Driver ID and bus ID required"}), 400

    if bus_id in buses:
        if buses[bus_id]['driver'] == driver_id:
            buses[bus_id]['driver'] = None
            buses[bus_id]['status'] = 'inactive'
            return jsonify({"status": "success", "message": "Driver logged out successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Driver not assigned to this bus"}), 400
    else:
        return jsonify({"status": "error", "message": "Bus not found"}), 404

@app.route('/student/login', methods=['POST'])
def login_student():
    """Student login."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    student_id = data.get('student_id')
    password = data.get('password')

    if not student_id or not password:
        return jsonify({"status": "error", "message": "Student ID and password required"}), 400

    if student_id in students and students[student_id]['password'] == password:
        return jsonify({
            "status": "success", 
            "message": "Student login successful",
            "studentName": students[student_id]['name']
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid student credentials"}), 401

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Server is running"}), 200

# ================== Run Server ==================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    
#     <!-- venv/Scripts/activate -->
#  <!-- uvicorn main:app --reload --host 0.0.0.0 --port 8000 -->