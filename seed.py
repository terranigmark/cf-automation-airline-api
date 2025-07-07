from datetime import timedelta
import random
from faker import Faker
import models, deps

faker = Faker()


def seed_airports(n=100):
    for _ in range(n):
        iata = faker.unique.lexify(text="???").upper()
        models.DB["airports"][iata] = {
            "iata_code": iata,
            "city": faker.city(),
            "country": faker.country(),
        }


def seed_aircrafts(n=50):
    ids = []
    for _ in range(n):
        aid = models.generate_id("acf")
        ids.append(aid)
        models.DB["aircrafts"][aid] = {
            "id": aid,
            "tail_number": faker.unique.bothify(text="??-####"),
            "model": f"{faker.word()} {random.randint(100, 999)}",
            "capacity": random.randint(100, 300),
        }
    return ids


def seed_flights(aircraft_ids, n=1000):
    airport_codes = list(models.DB["airports"].keys())
    for _ in range(n):
        origin, destination = random.sample(airport_codes, 2)
        departure = faker.date_time_between(start_date="now", end_date="+60d")
        arrival = departure + timedelta(hours=random.randint(1, 5))
        aid = random.choice(aircraft_ids)
        fid = models.generate_id("flt")
        capacity = models.DB["aircrafts"][aid]["capacity"]
        models.DB["flights"][fid] = {
            "id": fid,
            "origin": origin,
            "destination": destination,
            "departure_time": departure,
            "arrival_time": arrival,
            "base_price": round(random.uniform(100, 1000), 2),
            "aircraft_id": aid,
            "available_seats": capacity,
        }


def seed_users(n=10000):
    for _ in range(n):
        uid = models.generate_id("usr")
        models.DB["users"][uid] = {
            "id": uid,
            "email": faker.unique.email(),
            "password": deps.hash_password("pass1234"),
            "full_name": faker.name(),
            "role": models.Role.passenger,
        }


def seed_bookings(n=7000):
    flight_ids = list(models.DB["flights"].keys())
    user_ids = list(models.DB["users"].keys())
    for _ in range(n):
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
                    "seat": None,
                }
            ],
        }


def seed_payments(n=5000):
    booking_ids = list(models.DB["bookings"].keys())
    paid_bookings = random.sample(booking_ids, n)
    for bid in paid_bookings:
        pid = models.generate_id("pay")
        models.DB["payments"][pid] = {
            "id": pid,
            "booking_id": bid,
            "status": models.PaymentStatus.success,
        }
        models.DB["bookings"][bid]["status"] = models.BookingStatus.paid


def seed_all():
    seed_airports()
    aircraft_ids = seed_aircrafts()
    seed_flights(aircraft_ids)
    seed_users()
    seed_bookings()
    seed_payments()


if __name__ == "__main__":
    seed_all()
    print("Fake data generated")
