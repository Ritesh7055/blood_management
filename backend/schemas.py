from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# ── Donor ──────────────────────────────────────────────────
class DonorBase(BaseModel):
    name: str
    gender: Optional[str] = None
    age: Optional[int] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    last_donation_date: Optional[date] = None
    health_status: Optional[str] = "Healthy"

class DonorCreate(DonorBase): pass

class DonorUpdate(DonorBase): pass

class DonorOut(DonorBase):
    donor_id: int
    class Config: from_attributes = True

# ── DonationCamp ───────────────────────────────────────────
class CampBase(BaseModel):
    camp_name: str
    date: Optional[date] = None
    time: Optional[str] = None
    location: Optional[str] = None

class CampCreate(CampBase): pass
class CampUpdate(CampBase): pass

class CampOut(CampBase):
    camp_id: int
    class Config: from_attributes = True

# ── BloodDonation ──────────────────────────────────────────
class DonationBase(BaseModel):
    donation_date: Optional[date] = None
    blood_type: str
    quantity: float
    donor_id: int
    camp_id: Optional[int] = None

class DonationCreate(DonationBase): pass
class DonationUpdate(DonationBase): pass

class DonationOut(DonationBase):
    donation_id: int
    class Config: from_attributes = True

# ── BloodInventory ─────────────────────────────────────────
class InventoryBase(BaseModel):
    blood_type: str
    quantity: float
    collection_date: Optional[date] = None
    expiry_date: Optional[date] = None
    storage_location: Optional[str] = None
    status: Optional[str] = "Available"
    donation_id: Optional[int] = None

class InventoryCreate(InventoryBase): pass
class InventoryUpdate(InventoryBase): pass

class InventoryOut(InventoryBase):
    inventory_id: int
    class Config: from_attributes = True

# ── Hospital ───────────────────────────────────────────────
class HospitalBase(BaseModel):
    hospital_name: str
    address: Optional[str] = None
    contact_no: Optional[str] = None
    email: Optional[str] = None

class HospitalCreate(HospitalBase): pass
class HospitalUpdate(HospitalBase): pass

class HospitalOut(HospitalBase):
    hospital_id: int
    class Config: from_attributes = True

# ── BloodRequest ───────────────────────────────────────────
class RequestBase(BaseModel):
    request_date: Optional[date] = None
    blood_type: str
    quantity: float
    request_status: Optional[str] = "Pending"
    hospital_id: int

class RequestCreate(RequestBase): pass
class RequestUpdate(RequestBase): pass

class RequestOut(RequestBase):
    request_id: int
    class Config: from_attributes = True

# ── Admin ──────────────────────────────────────────────────
class AdminBase(BaseModel):
    admin_name: str
    email: str
    contact_no: Optional[str] = None

class AdminCreate(AdminBase):
    password: str

class AdminOut(AdminBase):
    admin_id: int
    class Config: from_attributes = True

# ── Dashboard Stats ────────────────────────────────────────
class DashboardStats(BaseModel):
    total_donors: int
    total_donations: int
    total_inventory: int
    pending_requests: int
    total_hospitals: int
    total_camps: int
    blood_group_summary: dict
