# 🩸 Blood Management System

A full-stack Blood Management System built with **FastAPI + SQLite** (backend) and **HTML/CSS/JS** (frontend), based on the ER diagram with 7 entities.

---

## 📁 Project Structure

```
blood_management/
├── backend/
│   ├── main.py           ← FastAPI app with all routes
│   ├── models.py         ← SQLAlchemy ORM models
│   ├── schemas.py        ← Pydantic request/response schemas
│   ├── database.py       ← DB connection & session
│   └── requirements.txt  ← Python dependencies
└── frontend/
    └── index.html        ← Single-page frontend UI
```

---

## 🚀 Setup & Run

### Step 1 — Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Run the backend

```bash
cd backend
python main.py
```

The API will start at: **http://localhost:8000**
Interactive API docs: **http://localhost:8000/docs**

### Step 3 — Open the frontend

Open `frontend/index.html` in any browser.

> **Note:** Make sure the backend is running before opening the frontend.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /dashboard | Summary stats |
| GET/POST | /donors | List / Create donors |
| GET/PUT/DELETE | /donors/{id} | Get / Update / Delete donor |
| GET/POST | /donations | Blood donations |
| GET/POST | /inventory | Blood inventory |
| GET/POST | /requests | Blood requests |
| PATCH | /requests/{id}/approve | Approve a request |
| PATCH | /requests/{id}/fulfill | Fulfill a request |
| GET/POST | /camps | Donation camps |
| GET/POST | /hospitals | Hospitals |

---

## 🗄️ Database

- Uses **SQLite** (file: `backend/blood_management.db`)
- Auto-created on first run with demo seed data
- 7 tables matching the ER diagram

## 🩸 Entities

| Entity | Primary Key |
|--------|-------------|
| Donor | donor_id |
| DonationCamp | camp_id |
| BloodDonation | donation_id |
| BloodInventory | inventory_id |
| Hospital | hospital_id |
| BloodRequest | request_id |
| Admin | admin_id |

---

## 💡 Features

- ✅ Full CRUD for all 6 entities
- ✅ Dashboard with live statistics
- ✅ Blood type availability chart
- ✅ Approve & fulfill blood requests
- ✅ Filter by blood type, status
- ✅ Demo data seeded automatically
- ✅ Toast notifications
- ✅ Responsive sidebar UI
"# blood_management" 
