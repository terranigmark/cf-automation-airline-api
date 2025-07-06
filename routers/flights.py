from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
import models, schemas, deps

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.post("", response_model=schemas.FlightOut, status_code=201)
def create_flight(flight: schemas.FlightCreate, _: dict = Depends(deps.require_admin)):
    fid = models.generate_id("flt")
    data = flight.dict()
    data |= {"id": fid, "available_seats": 150}
    models.DB["flights"][fid] = data
    return data

@router.get("", response_model=list[schemas.FlightOut])
def search_flights(
    origin: str | None = Query(None, min_length=3, max_length=3),
    destination: str | None = Query(None, min_length=3, max_length=3),
    date: datetime | None = None,
    p: dict = Depends(deps.pagination)
):
    flights = models.DB["flights"].values()
    if origin:
        flights = [f for f in flights if f["origin"] == origin]
    if destination:
        flights = [f for f in flights if f["destination"] == destination]
    if date:
        flights = [f for f in flights if f["departure_time"].date() == date.date()]
    return list(flights)[p["skip"]:p["skip"]+p["limit"]]

@router.get("/{flight_id}", response_model=schemas.FlightOut)
def get_flight(flight_id: str):
    fl = models.DB["flights"].get(flight_id)
    if not fl:
        raise HTTPException(status_code=404)
    return fl

@router.put("/{flight_id}", response_model=schemas.FlightOut)
def update_flight(flight_id: str, patch: schemas.FlightCreate, _: dict = Depends(deps.require_admin)):
    fl = models.DB["flights"].get(flight_id)
    if not fl:
        raise HTTPException(status_code=404)
    fl.update(patch.dict(exclude_unset=True))
    return fl

@router.delete("/{flight_id}", status_code=204)
def delete_flight(flight_id: str, _: dict = Depends(deps.require_admin)):
    models.DB["flights"].pop(flight_id, None)
