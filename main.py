from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# ================== CORS ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://astounding-gingersnap-c4eb35.netlify.app",  # your Netlify frontend
        "http://localhost:3000",   # React local dev
        "http://127.0.0.1:5500",   # VSCode Live Server
        "http://localhost:8000"    # optional for local API testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== Models ==================
class LocationUpdate(BaseModel):
    lat: float
    lng: float
    timestamp: Optional[str] = None

class DriverLogin(BaseModel):
    driver_id: str
    password: str
    bus_id: str

class DriverLogout(BaseModel):
    driver_id: str
    bus_id: str

class StudentLogin(BaseModel):
    student_id: str
    password: str

# ================== In-memory Data ==================
buses = {
    "1": {"lat": 12.9716, "lng": 77.5946, "name": "Campus Shuttle A", "status": "inactive",
          "lastUpdate": datetime.now().isoformat(), "driver": None},
    "2": {"lat": 12.9352, "lng": 77.6245, "name": "North Route", "status": "inactive",
          "lastUpdate": datetime.now().isoformat(), "driver": None},
    "3": {"lat": 12.9876, "lng": 77.5512, "name": "South Route", "status": "inactive",
          "lastUpdate": datetime.now().isoformat(), "driver": None},
    "4": {"lat": 12.9563, "lng": 77.5768, "name": "East Route", "status": "inactive",
          "lastUpdate": datetime.now().isoformat(), "driver": None}
}

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

@app.get("/buses")
async def get_buses():
    """Return all buses with latest location and status."""
    return buses

@app.post("/buses/{bus_id}/location")
async def update_bus_location(bus_id: str, location: LocationUpdate):
    """Drivers send their current location to update the server."""
    if bus_id not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    buses[bus_id]['lat'] = location.lat
    buses[bus_id]['lng'] = location.lng
    buses[bus_id]['status'] = 'active'
    buses[bus_id]['lastUpdate'] = location.timestamp or datetime.now().isoformat()
    
    return {"status": "success", "message": "Location updated", "bus": buses[bus_id]}

@app.post("/driver/login")
async def login_driver(login_data: DriverLogin):
    """Driver login: assign driver to their bus."""
    if login_data.driver_id not in drivers or drivers[login_data.driver_id]['password'] != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid driver credentials")
    
    if drivers[login_data.driver_id]['busId'] != login_data.bus_id:
        raise HTTPException(status_code=403, detail="Driver not assigned to this bus")
        
    buses[login_data.bus_id]['driver'] = login_data.driver_id
    buses[login_data.bus_id]['status'] = 'active'
    
    return {
        "status": "success", 
        "message": "Driver login successful", 
        "busId": login_data.bus_id,
        "driverName": drivers[login_data.driver_id]['name']
    }

@app.post("/driver/logout")
async def logout_driver(logout_data: DriverLogout):
    """Driver logout: release bus assignment."""
    if logout_data.bus_id not in buses:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    if buses[logout_data.bus_id]['driver'] != logout_data.driver_id:
        raise HTTPException(status_code=400, detail="Driver not assigned to this bus")
    
    buses[logout_data.bus_id]['driver'] = None
    buses[logout_data.bus_id]['status'] = 'inactive'
    
    return {"status": "success", "message": "Driver logged out successfully"}

@app.post("/student/login")
async def login_student(login_data: StudentLogin):
    """Student login."""
    if login_data.student_id not in students or students[login_data.student_id]['password'] != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid student credentials")
    
    return {
        "status": "success", 
        "message": "Student login successful",
        "studentName": students[login_data.student_id]['name']
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Server is running"}

# ================== Run Server ==================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#     <!-- venv/Scripts/activate -->
#  <!-- uvicorn main:app --reload --host 0.0.0.0 --port 8000 -->