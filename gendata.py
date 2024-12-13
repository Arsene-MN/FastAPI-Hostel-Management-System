from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from uuid import uuid4
from faker import Faker
import random

# SQLite database configuration
DATABASE_URL = "sqlite:///hostel_management.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Define models for Hostel Management System
class Hostel(Base):
    __tablename__ = "hostels"
    hostel_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, nullable=False)
    rooms = relationship("Room", back_populates="hostel")

class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(String, primary_key=True, index=True)
    room_type = Column(String, nullable=False)
    price = Column(Float)
    availability = Column(Integer, default=1)
    hostel_id = Column(String, ForeignKey("hostels.hostel_id"))
    hostel = relationship("Hostel", back_populates="rooms")

# Faker instance for generating random data
fake = Faker()

# Seed data function
def seed_data(session: Session, num_hostels=10_000, total_rooms=500_000, batch_size=2_000):
    rooms_per_hostel = total_rooms // num_hostels
    leftover_rooms = total_rooms % num_hostels

    # Create and insert hostels in batches
    hostels = []
    total_hostels_added = 0
    for i in range(num_hostels):
        hostel = Hostel(
            hostel_id=str(uuid4()),
            name=fake.company(),
            location=fake.city()
        )
        hostels.append(hostel)
        if len(hostels) >= batch_size:
            session.bulk_save_objects(hostels)
            session.commit()
            total_hostels_added += len(hostels)
            print(f"{total_hostels_added} hostels added...")
            hostels = []
    if hostels:
        session.bulk_save_objects(hostels)
        session.commit()
        total_hostels_added += len(hostels)
        print(f"{total_hostels_added} hostels added.")
    
    # Create and insert rooms in batches
    rooms = []
    room_count = 0
    for hostel in session.query(Hostel).all():
        num_rooms = rooms_per_hostel + (1 if leftover_rooms > 0 else 0)
        if leftover_rooms > 0:
            leftover_rooms -= 1
        for _ in range(num_rooms):
            room_count += 1
            room = Room(
                room_id=str(uuid4()),
                room_type=fake.random_element(elements=["Single", "Double", "Suite"]),
                price=random.uniform(30.0, 150.0),
                availability=random.randint(0, 1),
                hostel_id=hostel.hostel_id
            )
            rooms.append(room)
            if len(rooms) >= batch_size:
                session.bulk_save_objects(rooms)
                session.commit()
                print(f"{room_count} rooms added...")
                rooms = []
    if rooms:
        session.bulk_save_objects(rooms)
        session.commit()
        print(f"{room_count} rooms added.")

if __name__ == "__main__":
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Initialize database session
    db_session = Session(bind=engine)
    try:
        seed_data(db_session, num_hostels=10_000, total_rooms=50_000, batch_size=2_000)
    finally:
        db_session.close()
