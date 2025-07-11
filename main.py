import seed
from fastapi import FastAPI
from routers import auth, users, airports, flights, bookings, payments, aircrafts
import models, deps

app = FastAPI(
    title="Airline Demo API",
    version="0.2.0",
    description="Bootcamp FastAPI demo for airline flight purchase & management"
)

# --- Seed an initial admin user (for demo purposes only) ---
def seed_admin():
    if any(u["role"] == models.Role.admin for u in models.DB["users"].values()):
        return
    uid = models.generate_id("usr")
    models.DB["users"][uid] = {
        "id": uid,
        "email": "admin@demo.com",
        "password": deps.hash_password("admin123"),
        "full_name": "Bootcamp Admin",
        "role": models.Role.admin,
    }

seed_admin()

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(airports.router)
app.include_router(flights.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(aircrafts.router)

@app.get("/")
def root():
    return {"msg": "Airline API up & running"}

@app.on_event("startup")
async def run_seed_if_needed():
    await seed.seed_all()