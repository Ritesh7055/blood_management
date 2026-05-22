from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import date, timedelta

from database import get_db, init_db
from models import Donor, BloodDonation, DonationCamp, BloodInventory, Hospital, BloodRequest, Admin
from schemas import (
    DonorCreate, DonorUpdate, DonorOut,
    CampCreate, CampUpdate, CampOut,
    DonationCreate, DonationUpdate, DonationOut,
    InventoryCreate, InventoryUpdate, InventoryOut,
    HospitalCreate, HospitalUpdate, HospitalOut,
    RequestCreate, RequestUpdate, RequestOut,
    AdminCreate, AdminOut,
    DashboardStats
)

app = FastAPI(title="Blood Management System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    seed_demo_data()

def seed_demo_data():
    from database import SessionLocal
    db = SessionLocal()
    try:
        if db.query(Admin).count() == 0:
            admin = Admin(admin_name="Admin", email="admin@bms.com", password="admin123", contact_no="9999999999")
            db.add(admin)

        if db.query(Hospital).count() == 0:
            hospitals = [
                Hospital(hospital_name="City General Hospital", address="MG Road, Jaipur", contact_no="0141-2200000", email="city@hospital.com"),
                Hospital(hospital_name="Fortis Hospital", address="JLN Marg, Jaipur", contact_no="0141-2500000", email="fortis@hospital.com"),
                Hospital(hospital_name="SMS Medical College", address="Sawai Ram Singh Rd, Jaipur", contact_no="0141-2518888", email="sms@hospital.com"),
            ]
            db.add_all(hospitals)

        if db.query(Donor).count() == 0:
            donors = [
                Donor(name="Rahul Sharma", gender="Male", age=28, mobile="9876543210", email="rahul@email.com", address="Vaishali Nagar, Jaipur", blood_group="A+", health_status="Healthy"),
                Donor(name="Priya Singh", gender="Female", age=24, mobile="9876543211", email="priya@email.com", address="Malviya Nagar, Jaipur", blood_group="B+", health_status="Healthy"),
                Donor(name="Amit Kumar", gender="Male", age=32, mobile="9876543212", email="amit@email.com", address="C-Scheme, Jaipur", blood_group="O+", health_status="Healthy"),
                Donor(name="Sneha Patel", gender="Female", age=26, mobile="9876543213", email="sneha@email.com", address="Mansarovar, Jaipur", blood_group="AB+", health_status="Healthy"),
                Donor(name="Vikram Joshi", gender="Male", age=30, mobile="9876543214", email="vikram@email.com", address="Sodala, Jaipur", blood_group="O-", health_status="Healthy"),
            ]
            db.add_all(donors)

        if db.query(DonationCamp).count() == 0:
            camps = [
                DonationCamp(camp_name="Jaipur Blood Drive 2026", date=date(2026, 5, 20), time="09:00 AM", location="Central Park, Jaipur"),
                DonationCamp(camp_name="World Blood Donor Day Camp", date=date(2026, 6, 14), time="10:00 AM", location="SMS Hospital Grounds"),
            ]
            db.add_all(camps)

        db.commit()

        if db.query(BloodDonation).count() == 0:
            donations = [
                BloodDonation(donation_date=date(2026, 4, 10), blood_type="A+", quantity=350, donor_id=1, camp_id=1),
                BloodDonation(donation_date=date(2026, 4, 12), blood_type="B+", quantity=350, donor_id=2, camp_id=1),
                BloodDonation(donation_date=date(2026, 4, 15), blood_type="O+", quantity=350, donor_id=3, camp_id=None),
                BloodDonation(donation_date=date(2026, 5, 1), blood_type="AB+", quantity=350, donor_id=4, camp_id=2),
                BloodDonation(donation_date=date(2026, 5, 5), blood_type="O-", quantity=350, donor_id=5, camp_id=None),
            ]
            db.add_all(donations)
            db.commit()

        if db.query(BloodInventory).count() == 0:
            inventory = [
                BloodInventory(blood_type="A+", quantity=350, collection_date=date(2026, 4, 10), expiry_date=date(2026, 5, 10), storage_location="Shelf A1", status="Available", donation_id=1),
                BloodInventory(blood_type="B+", quantity=350, collection_date=date(2026, 4, 12), expiry_date=date(2026, 5, 12), storage_location="Shelf B1", status="Available", donation_id=2),
                BloodInventory(blood_type="O+", quantity=350, collection_date=date(2026, 4, 15), expiry_date=date(2026, 5, 15), storage_location="Shelf C1", status="Used", donation_id=3),
                BloodInventory(blood_type="AB+", quantity=350, collection_date=date(2026, 5, 1), expiry_date=date(2026, 6, 1), storage_location="Shelf D1", status="Available", donation_id=4),
                BloodInventory(blood_type="O-", quantity=350, collection_date=date(2026, 5, 5), expiry_date=date(2026, 6, 5), storage_location="Shelf E1", status="Available", donation_id=5),
            ]
            db.add_all(inventory)

        if db.query(BloodRequest).count() == 0:
            requests = [
                BloodRequest(request_date=date(2026, 5, 10), blood_type="A+", quantity=200, request_status="Pending", hospital_id=1),
                BloodRequest(request_date=date(2026, 5, 12), blood_type="O+", quantity=350, request_status="Fulfilled", hospital_id=2),
                BloodRequest(request_date=date(2026, 5, 14), blood_type="B+", quantity=150, request_status="Approved", hospital_id=3),
            ]
            db.add_all(requests)

        db.commit()
    finally:
        db.close()

# ── Dashboard ──────────────────────────────────────────────
@app.get("/dashboard", response_model=DashboardStats)
def get_dashboard(db: Session = Depends(get_db)):
    blood_groups = db.query(BloodInventory.blood_type, func.sum(BloodInventory.quantity))\
        .filter(BloodInventory.status == "Available")\
        .group_by(BloodInventory.blood_type).all()
    return DashboardStats(
        total_donors=db.query(Donor).count(),
        total_donations=db.query(BloodDonation).count(),
        total_inventory=db.query(BloodInventory).filter(BloodInventory.status == "Available").count(),
        pending_requests=db.query(BloodRequest).filter(BloodRequest.request_status == "Pending").count(),
        total_hospitals=db.query(Hospital).count(),
        total_camps=db.query(DonationCamp).count(),
        blood_group_summary={bg: float(qty) for bg, qty in blood_groups}
    )

# ── Donors ─────────────────────────────────────────────────
@app.get("/donors", response_model=List[DonorOut])
def list_donors(search: Optional[str] = None, blood_group: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Donor)
    if search:
        q = q.filter(Donor.name.ilike(f"%{search}%") | Donor.email.ilike(f"%{search}%"))
    if blood_group:
        q = q.filter(Donor.blood_group == blood_group)
    return q.all()

@app.get("/donors/{donor_id}", response_model=DonorOut)
def get_donor(donor_id: int, db: Session = Depends(get_db)):
    d = db.query(Donor).filter(Donor.donor_id == donor_id).first()
    if not d: raise HTTPException(404, "Donor not found")
    return d

@app.post("/donors", response_model=DonorOut, status_code=201)
def create_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    d = Donor(**donor.model_dump())
    db.add(d); db.commit(); db.refresh(d)
    return d

@app.put("/donors/{donor_id}", response_model=DonorOut)
def update_donor(donor_id: int, donor: DonorUpdate, db: Session = Depends(get_db)):
    d = db.query(Donor).filter(Donor.donor_id == donor_id).first()
    if not d: raise HTTPException(404, "Donor not found")
    for k, v in donor.model_dump().items():
        setattr(d, k, v)
    db.commit(); db.refresh(d); return d

@app.delete("/donors/{donor_id}")
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    d = db.query(Donor).filter(Donor.donor_id == donor_id).first()
    if not d: raise HTTPException(404, "Donor not found")
    db.delete(d); db.commit()
    return {"message": "Deleted successfully"}

# ── Donation Camps ─────────────────────────────────────────
@app.get("/camps", response_model=List[CampOut])
def list_camps(db: Session = Depends(get_db)):
    return db.query(DonationCamp).all()

@app.get("/camps/{camp_id}", response_model=CampOut)
def get_camp(camp_id: int, db: Session = Depends(get_db)):
    c = db.query(DonationCamp).filter(DonationCamp.camp_id == camp_id).first()
    if not c: raise HTTPException(404, "Camp not found")
    return c

@app.post("/camps", response_model=CampOut, status_code=201)
def create_camp(camp: CampCreate, db: Session = Depends(get_db)):
    c = DonationCamp(**camp.model_dump())
    db.add(c); db.commit(); db.refresh(c); return c

@app.put("/camps/{camp_id}", response_model=CampOut)
def update_camp(camp_id: int, camp: CampUpdate, db: Session = Depends(get_db)):
    c = db.query(DonationCamp).filter(DonationCamp.camp_id == camp_id).first()
    if not c: raise HTTPException(404, "Camp not found")
    for k, v in camp.model_dump().items(): setattr(c, k, v)
    db.commit(); db.refresh(c); return c

@app.delete("/camps/{camp_id}")
def delete_camp(camp_id: int, db: Session = Depends(get_db)):
    c = db.query(DonationCamp).filter(DonationCamp.camp_id == camp_id).first()
    if not c: raise HTTPException(404, "Camp not found")
    db.delete(c); db.commit(); return {"message": "Deleted"}

# ── Blood Donations ────────────────────────────────────────
@app.get("/donations", response_model=List[DonationOut])
def list_donations(blood_type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(BloodDonation)
    if blood_type: q = q.filter(BloodDonation.blood_type == blood_type)
    return q.all()

@app.post("/donations", response_model=DonationOut, status_code=201)
def create_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    d = BloodDonation(**donation.model_dump())
    db.add(d); db.commit(); db.refresh(d)
    donor = db.query(Donor).filter(Donor.donor_id == donation.donor_id).first()
    if donor: donor.last_donation_date = donation.donation_date or date.today()
    db.commit()
    return d

@app.put("/donations/{donation_id}", response_model=DonationOut)
def update_donation(donation_id: int, donation: DonationUpdate, db: Session = Depends(get_db)):
    d = db.query(BloodDonation).filter(BloodDonation.donation_id == donation_id).first()
    if not d: raise HTTPException(404, "Not found")
    for k, v in donation.model_dump().items(): setattr(d, k, v)
    db.commit(); db.refresh(d); return d

@app.delete("/donations/{donation_id}")
def delete_donation(donation_id: int, db: Session = Depends(get_db)):
    d = db.query(BloodDonation).filter(BloodDonation.donation_id == donation_id).first()
    if not d: raise HTTPException(404, "Not found")
    db.delete(d); db.commit(); return {"message": "Deleted"}

# ── Blood Inventory ────────────────────────────────────────
@app.get("/inventory", response_model=List[InventoryOut])
def list_inventory(status: Optional[str] = None, blood_type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(BloodInventory)
    if status: q = q.filter(BloodInventory.status == status)
    if blood_type: q = q.filter(BloodInventory.blood_type == blood_type)
    return q.all()

@app.post("/inventory", response_model=InventoryOut, status_code=201)
def create_inventory(inv: InventoryCreate, db: Session = Depends(get_db)):
    i = BloodInventory(**inv.model_dump())
    db.add(i); db.commit(); db.refresh(i); return i

@app.put("/inventory/{inventory_id}", response_model=InventoryOut)
def update_inventory(inventory_id: int, inv: InventoryUpdate, db: Session = Depends(get_db)):
    i = db.query(BloodInventory).filter(BloodInventory.inventory_id == inventory_id).first()
    if not i: raise HTTPException(404, "Not found")
    for k, v in inv.model_dump().items(): setattr(i, k, v)
    db.commit(); db.refresh(i); return i

@app.delete("/inventory/{inventory_id}")
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    i = db.query(BloodInventory).filter(BloodInventory.inventory_id == inventory_id).first()
    if not i: raise HTTPException(404, "Not found")
    db.delete(i); db.commit(); return {"message": "Deleted"}

# ── Hospitals ──────────────────────────────────────────────
@app.get("/hospitals", response_model=List[HospitalOut])
def list_hospitals(db: Session = Depends(get_db)):
    return db.query(Hospital).all()

@app.post("/hospitals", response_model=HospitalOut, status_code=201)
def create_hospital(h: HospitalCreate, db: Session = Depends(get_db)):
    hosp = Hospital(**h.model_dump())
    db.add(hosp); db.commit(); db.refresh(hosp); return hosp

@app.put("/hospitals/{hospital_id}", response_model=HospitalOut)
def update_hospital(hospital_id: int, h: HospitalUpdate, db: Session = Depends(get_db)):
    hosp = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hosp: raise HTTPException(404, "Not found")
    for k, v in h.model_dump().items(): setattr(hosp, k, v)
    db.commit(); db.refresh(hosp); return hosp

@app.delete("/hospitals/{hospital_id}")
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hosp = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hosp: raise HTTPException(404, "Not found")
    db.delete(hosp); db.commit(); return {"message": "Deleted"}

# ── Blood Requests ─────────────────────────────────────────
@app.get("/requests", response_model=List[RequestOut])
def list_requests(status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(BloodRequest)
    if status: q = q.filter(BloodRequest.request_status == status)
    return q.all()

@app.post("/requests", response_model=RequestOut, status_code=201)
def create_request(req: RequestCreate, db: Session = Depends(get_db)):
    r = BloodRequest(**req.model_dump())
    db.add(r); db.commit(); db.refresh(r); return r

@app.put("/requests/{request_id}", response_model=RequestOut)
def update_request(request_id: int, req: RequestUpdate, db: Session = Depends(get_db)):
    r = db.query(BloodRequest).filter(BloodRequest.request_id == request_id).first()
    if not r: raise HTTPException(404, "Not found")
    for k, v in req.model_dump().items(): setattr(r, k, v)
    db.commit(); db.refresh(r); return r

@app.delete("/requests/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    r = db.query(BloodRequest).filter(BloodRequest.request_id == request_id).first()
    if not r: raise HTTPException(404, "Not found")
    db.delete(r); db.commit(); return {"message": "Deleted"}

@app.patch("/requests/{request_id}/approve")
def approve_request(request_id: int, db: Session = Depends(get_db)):
    r = db.query(BloodRequest).filter(BloodRequest.request_id == request_id).first()
    if not r: raise HTTPException(404, "Not found")
    r.request_status = "Approved"
    db.commit(); db.refresh(r); return r

@app.patch("/requests/{request_id}/fulfill")
def fulfill_request(request_id: int, db: Session = Depends(get_db)):
    r = db.query(BloodRequest).filter(BloodRequest.request_id == request_id).first()
    if not r: raise HTTPException(404, "Not found")
    inv = db.query(BloodInventory).filter(
        BloodInventory.blood_type == r.blood_type,
        BloodInventory.status == "Available"
    ).first()
    if not inv: raise HTTPException(400, "No available inventory for this blood type")
    inv.status = "Used"
    r.request_status = "Fulfilled"
    db.commit(); return {"message": "Request fulfilled"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
