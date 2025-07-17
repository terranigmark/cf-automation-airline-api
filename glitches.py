import random
import time
from fastapi import HTTPException
from fastapi.responses import JSONResponse


def maybe_bug():
    """Randomly return or raise various simulated errors."""
    r = random.random()
    if r < 0.0075:
        return JSONResponse({"detail": "Error 400"}, status_code=200)
    elif r < 0.015:
        raise HTTPException(status_code=400, detail="Simulated 4xx bug")
    elif r < 0.0225:
        raise HTTPException(status_code=500, detail="Simulated 5xx bug")
    elif r < 0.03:
        # Simulate a timeout by sleeping for a moment before raising
        time.sleep(2)
        raise HTTPException(status_code=504, detail="Simulated timeout")
    return None


def maybe_corrupt_passengers(data: dict) -> dict:
    """Randomly set passenger full names to None."""
    if random.random() < 0.3:
        for passenger in data.get("passengers", []):
            if random.random() < 0.5:
                passenger["full_name"] = None
    return data


def _maybe_corrupt_fields(data: dict, fields: list[str]) -> dict:
    """Randomly set some fields to None."""
    if random.random() < 0.3:
        for f in fields:
            if f in data and random.random() < 0.5:
                data[f] = None
    return data


def maybe_corrupt_airport(data: dict) -> dict:
    return _maybe_corrupt_fields(data, ["city", "country"])


def maybe_corrupt_flight(data: dict) -> dict:
    return _maybe_corrupt_fields(data, ["origin", "destination", "available_seats"])


def maybe_corrupt_booking(data: dict) -> dict:
    _maybe_corrupt_fields(data, ["status"])  # mutate in place
    return maybe_corrupt_passengers(data)


def maybe_corrupt_payment(data: dict) -> dict:
    return _maybe_corrupt_fields(data, ["status"])


def maybe_corrupt_aircraft(data: dict) -> dict:
    return _maybe_corrupt_fields(data, ["model", "capacity"])


def maybe_corrupt_user(data: dict) -> dict:
    return _maybe_corrupt_fields(data, ["full_name", "email"])
