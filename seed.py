"""
Sembrado de datos “seguro”:
- Idempotente: solo si las colecciones están vacías.
- Volumen controlado mediante la variable FAST_SEED (true/false).
- Logs reducidos para no saturar Render.
"""

import os, random, logging
from datetime import timedelta
from faker import Faker
import models, deps

faker = Faker()
log = logging.getLogger("seed")

# ---------- Parámetros ---------- #
FAST = os.getenv("FAST_SEED", "true").lower() == "true"

CNT = {
    "airports": 20 if FAST else 100,
    "aircrafts": 10 if FAST else 50,
    "flights": 200 if FAST else 1000,
    "users": 50 if FAST else 200,
    "bookings": 300 if FAST else 7000,
    "payments": 200 if FAST else 5000,
}


# ---------- Helpers ---------- #
def _log_every(i: int, total: int):
    if i % 10 == 0 or i == total - 1:
        log.info("…%s/%s", i + 1, total)


# ---------- Seeders ---------- #
def seed_airports():
    if models.DB["airports"]:
        return
    n = CNT["airports"]
    log.info("Seeding %s airports…", n)
    for i in range(n):
        iata = faker.unique.lexify(text="???").upper()
        models.DB["airports"][iata] = {
            "iata_code": iata,
            "city": faker.city(),
            "country": faker.country(),
        }
        _log_every(i, n)


def seed_aircrafts() -> list[str]:
    if models.DB["aircrafts"]:
        return list(models.DB["aircrafts"].keys())
    n = CNT["aircrafts"]
    log.info("Seeding %s aircrafts…", n)
    ids = []
    for i in range(n):
        aid = models.generate_id("acf")
        ids.append(aid)
        models.DB["aircrafts"][aid] = {
            "id": aid,
            "tail_number": faker.unique.bothify(text="??-####"),
            "model": f"{faker.word()} {random.randint(100, 999)}",
            "capacity": random.randint(100, 300),
        }
        _log_every(i, n)
    return ids


def seed_flights(aircraft_ids: list[str]):
    if models.DB["flights"]:
        return
    n = CNT["flights"]
    log.info("Seeding %s flights…", n)
    airport_codes = list(models.DB["airports"].keys())
    for i in range(n):
        origin, destination = random.sample(airport_codes, 2)
        departure = faker.date_time_between(start_date="now", end_date="+60d")
        arrival = departure + timedelta(hours=random.randint(1, 5))
        fid = models.generate_id("flt")
        aid = random.choice(aircraft_ids)
        models.DB["flights"][fid] = {
            "id": fid,
            "origin": origin,
            "destination": destination,
            "departure_time": departure,
            "arrival_time": arrival,
            "base_price": round(random.uniform(100, 1000), 2),
            "aircraft_id": aid,
            "available_seats": models.DB["aircrafts"][aid]["capacity"],
        }
        _log_every(i, n)


def seed_users():
    if models.DB["users"]:
        return
    n = CNT["users"]
    log.info("Seeding %s users…", n)
    for i in range(n):
        uid = models.generate_id("usr")
        models.DB["users"][uid] = {
            "id": uid,
            "email": faker.unique.email(),
            "password": deps.hash_password("pass1234"),
            "full_name": faker.name(),
            "role": models.Role.passenger,
        }
        _log_every(i, n)


def seed_bookings():
    if models.DB["bookings"]:
        return
    n = CNT["bookings"]
    log.info("Seeding %s bookings…", n)
    flight_ids = list(models.DB["flights"].keys())
    user_ids = list(models.DB["users"].keys())
    for i in range(n):
        bid = models.generate_id("bkg")
        models.DB["bookings"][bid] = {
            "id": bid,
            "flight_id": random.choice(flight_ids),
            "user_id": random.choice(user_ids),
            "status": models.BookingStatus.draft,
            "passengers": [
                {
                    "full_name": faker.name(),
                    "passport": faker.bothify(text="????????"),
                    "seat": f"{random.randint(1, 45)}{random.choice('ABCDEF')}",
                }
            ],
        }
        _log_every(i, n)


def seed_payments():
    if models.DB["payments"]:
        return
    n = CNT["payments"]
    log.info("Seeding %s payments…", n)
    booking_ids = list(models.DB["bookings"].keys())
    paid_bookings = random.sample(booking_ids, min(n, len(booking_ids)))
    for i, bid in enumerate(paid_bookings):
        pid = models.generate_id("pay")
        models.DB["payments"][pid] = {
            "id": pid,
            "booking_id": bid,
            "status": models.PaymentStatus.success,
        }
        models.DB["bookings"][bid]["status"] = models.BookingStatus.paid
        _log_every(i, n)


async def run_if_needed():
    """Ejecuta todos los seeders de forma segura e idempotente."""
    seed_airports()
    aids = seed_aircrafts()
    seed_flights(aids)
    seed_users()
    seed_bookings()
    seed_payments()
    log.info("✅ Seed completo")
