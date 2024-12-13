from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
from passlib.context import CryptContext
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import httpx
import math

# Constants
# SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_FILE = "database.json"

# Initialize FastAPI app
app = FastAPI(title="Hostel Management System API", description="API for managing hostels, rooms, and bookings")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class HostelBase(BaseModel):
    name: str
    location: str

class HostelCreate(HostelBase):
    pass

class Hostel(HostelBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    hostel_id: int
    number: str
    capacity: int

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    available: bool

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    room_id: int
    guest_name: str
    guest_email: EmailStr
    check_in_date: datetime
    check_out_date: datetime

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True

# Utility functions
def read_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Remove authentication for now
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Utility function to serialize datetime objects
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

# Utility function to clean NaN and Infinite values
def clean_data(data):
    if isinstance(data, dict):
        return {key: clean_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    elif isinstance(data, float) and (math.isnan(data) or math.isinf(data)):
        return None  # or replace with 0, depending on your requirement
    return data

# API Endpoints
@app.post("/signup/", response_model=User)
def create_user(user: UserCreate):
    db = read_db()
    if any(u["email"] == user.email for u in db["users"]):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "id": len(db["users"]) + 1,
        "username": user.username,
        "email": user.email,
        "hashed_password": get_password_hash(user.password)
    }
    db["users"].append(new_user)
    write_db(db)
    return new_user

@app.post("/hostels/", response_model=List[Hostel])  # Updated to accept multiple hostels
def create_hostels(hostels: List[HostelCreate]):  # Accepting a list of hostels
    db = read_db()
    new_hostels = []
    for hostel in hostels:
        new_hostel = {
            "id": len(db["hostels"]) + 1,
            "name": hostel.name,
            "location": hostel.location,
            "owner_id": 1  # Default owner as 1
        }
        db["hostels"].append(new_hostel)
        new_hostels.append(new_hostel)
    write_db(db)
    return new_hostels

@app.get("/hostels/", response_model=List[Hostel])  # Get all hostels without pagination
def read_hostels():
    db = read_db()
    return db["hostels"]

@app.post("/rooms/", response_model=List[Room])  # Updated to accept multiple rooms
def create_rooms(rooms: List[RoomCreate]):  # Accepting a list of rooms
    db = read_db()
    new_rooms = []
    for room in rooms:
        new_room = {
            "id": len(db["rooms"]) + 1,
            "hostel_id": room.hostel_id,
            "number": room.number,
            "capacity": room.capacity,
            "available": True
        }
        db["rooms"].append(new_room)
        new_rooms.append(new_room)
    write_db(db)
    return new_rooms

@app.get("/rooms/", response_model=List[Room])  # Get all rooms without pagination
def read_rooms():
    db = read_db()
    return db["rooms"]

@app.post("/bookings/", response_model=List[Booking])  # Updated to accept multiple bookings
def create_bookings(bookings: List[BookingCreate]):  # Accepting a list of bookings
    db = read_db()
    new_bookings = []
    for booking in bookings:
        room = next((r for r in db["rooms"] if r["id"] == booking.room_id and r["available"]), None)
        if not room:
            raise HTTPException(status_code=400, detail="Room is not available")
        
        room["available"] = False  # Mark room as booked
        new_booking = {
            "id": len(db["bookings"]) + 1,
            "room_id": booking.room_id,
            "guest_name": booking.guest_name,
            "guest_email": booking.guest_email,
            "check_in_date": booking.check_in_date.isoformat(),
            "check_out_date": booking.check_out_date.isoformat()
        }
        db["bookings"].append(new_booking)
        new_bookings.append(new_booking)
    write_db(db)
    return new_bookings

@app.get("/bookings/", response_model=List[Booking])  # Get all bookings without pagination
def read_bookings():
    db = read_db()
    bookings = db["bookings"]
    for booking in bookings:
        booking["check_in_date"] = datetime.fromisoformat(booking["check_in_date"])
        booking["check_out_date"] = datetime.fromisoformat(booking["check_out_date"])
    return bookings
