from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import date, datetime
import enum

Base = declarative_base()

class BloodGroup(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

class InventoryStatus(str, enum.Enum):
    AVAILABLE = "Available"
    USED = "Used"
    EXPIRED = "Expired"

class RequestStatus(str, enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    FULFILLED = "Fulfilled"
    REJECTED = "Rejected"

class Donor(Base):
    __tablename__ = "donors"
    donor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(10))
    age = Column(Integer)
    mobile = Column(String(15))
    email = Column(String(100), unique=True)
    address = Column(Text)
    blood_group = Column(String(5))
    last_donation_date = Column(Date, nullable=True)
    health_status = Column(String(50), default="Healthy")

    donations = relationship("BloodDonation", back_populates="donor")

class DonationCamp(Base):
    __tablename__ = "donation_camps"
    camp_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    camp_name = Column(String(100), nullable=False)
    date = Column(Date)
    time = Column(String(20))
    location = Column(String(200))

    donations = relationship("BloodDonation", back_populates="camp")

class BloodDonation(Base):
    __tablename__ = "blood_donations"
    donation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    donation_date = Column(Date, default=date.today)
    blood_type = Column(String(5))
    quantity = Column(Float)  # in units/ml
    donor_id = Column(Integer, ForeignKey("donors.donor_id"))
    camp_id = Column(Integer, ForeignKey("donation_camps.camp_id"), nullable=True)

    donor = relationship("Donor", back_populates="donations")
    camp = relationship("DonationCamp", back_populates="donations")
    inventory = relationship("BloodInventory", back_populates="donation", uselist=False)

class BloodInventory(Base):
    __tablename__ = "blood_inventory"
    inventory_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    blood_type = Column(String(5))
    quantity = Column(Float)
    collection_date = Column(Date)
    expiry_date = Column(Date)
    storage_location = Column(String(100))
    status = Column(String(20), default="Available")
    donation_id = Column(Integer, ForeignKey("blood_donations.donation_id"), nullable=True)

    donation = relationship("BloodDonation", back_populates="inventory")

class Hospital(Base):
    __tablename__ = "hospitals"
    hospital_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hospital_name = Column(String(150), nullable=False)
    address = Column(Text)
    contact_no = Column(String(15))
    email = Column(String(100))

    requests = relationship("BloodRequest", back_populates="hospital")

class BloodRequest(Base):
    __tablename__ = "blood_requests"
    request_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    request_date = Column(Date, default=date.today)
    blood_type = Column(String(5))
    quantity = Column(Float)
    request_status = Column(String(20), default="Pending")
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"))

    hospital = relationship("Hospital", back_populates="requests")

class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    admin_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String(200))
    contact_no = Column(String(15))
