from contextlib import asynccontextmanager
from fastapi import FastAPI
import models, deps, seed
from routers import auth, users, airports, flights, bookings, payments, aircrafts

# ---------- Lifespan ---------- #
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Siembra admin fijo
    if not any(u["role"] == models.Role.admin for u in models.DB["users"].values()):
        uid = models.generate_id("usr")
        models.DB["users"][uid] = {
            "id": uid,
            "email": "admin@demo.com",
            "password": deps.hash_password("admin123"),
            "full_name": "Bootcamp Admin",
            "role": models.Role.admin,
        }

    # Siembra datos fake (no bloquea si ya están)
    try:
        await seed.run_if_needed()
    except Exception as e:
        app.logger.error(f"Seed error: {e}")

    yield  # ---- aquí arranca la app ----
    # (opcional) código de shutdown


app = FastAPI(
    title="Airline Demo API",
    version="0.3.0",
    description="Bootcamp FastAPI demo for airline flight purchase & management",
    lifespan=lifespan,
)

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
