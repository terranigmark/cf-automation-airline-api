from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
import models, schemas, deps
import glitches

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.post("", response_model=schemas.FlightOut, status_code=201)
def create_flight(
    flight: schemas.FlightCreate, _: dict = Depends(deps.require_admin)
):
    if flight.aircraft_id not in models.DB["aircrafts"]:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    fid = models.generate_id("flt")
    data = flight.dict()
    capacity = models.DB["aircrafts"][flight.aircraft_id]["capacity"]
    data |= {"id": fid, "available_seats": capacity}
    models.DB["flights"][fid] = data
    return glitches.maybe_corrupt_flight(data)

@router.get("", response_model=list[schemas.FlightOut])
def search_flights(
    origin: str | None = Query(None, min_length=3, max_length=3),
    destination: str | None = Query(None, min_length=3, max_length=3),
    date: datetime | None = None,
    p: dict = Depends(deps.pagination)
):
    bug = glitches.maybe_bug()
    if bug:
        return bug
    flights = models.DB["flights"].values()
    if origin:
        flights = [f for f in flights if f["origin"] == origin]
    if destination:
        flights = [f for f in flights if f["destination"] == destination]
    if date:
        flights = [f for f in flights if f["departure_time"].date() == date.date()]
    flights = list(flights)[p["skip"]:p["skip"]+p["limit"]]
    return [glitches.maybe_corrupt_flight(dict(f)) for f in flights]

@router.get("/{flight_id}", response_model=schemas.FlightOut)
def get_flight(flight_id: str):
    bug = glitches.maybe_bug()
    if bug:
        return bug
    fl = models.DB["flights"].get(flight_id)
    if not fl:
        raise HTTPException(status_code=404)
    return glitches.maybe_corrupt_flight(dict(fl))

@router.put("/{flight_id}", response_model=schemas.FlightOut)
def update_flight(flight_id: str, patch: schemas.FlightCreate, _: dict = Depends(deps.require_admin)):
    fl = models.DB["flights"].get(flight_id)
    if not fl:
        raise HTTPException(status_code=404)
    changes = patch.dict(exclude_unset=True)
    if "aircraft_id" in changes:
        if changes["aircraft_id"] not in models.DB["aircrafts"]:
            raise HTTPException(status_code=404, detail="Aircraft not found")
        capacity = models.DB["aircrafts"][changes["aircraft_id"]]["capacity"]
        fl["available_seats"] = capacity
    fl.update(changes)
    return glitches.maybe_corrupt_flight(dict(fl))

@router.delete("/{flight_id}", status_code=204)
def delete_flight(flight_id: str, _: dict = Depends(deps.require_admin)):
    models.DB["flights"].pop(flight_id, None)
