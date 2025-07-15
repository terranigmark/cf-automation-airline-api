from fastapi import APIRouter, Depends, HTTPException
import models, schemas, deps
import glitches

router = APIRouter(prefix="/aircrafts", tags=["Aircrafts"])

@router.post("", response_model=schemas.AircraftOut, status_code=201)
def create_aircraft(ac: schemas.AircraftCreate, _: dict = Depends(deps.require_admin)):
    aid = models.generate_id("acf")
    data = ac.dict()
    data["id"] = aid
    models.DB["aircrafts"][aid] = data
    return glitches.maybe_corrupt_aircraft(data)

@router.get("", response_model=list[schemas.AircraftOut])
def list_aircrafts(p: dict = Depends(deps.pagination)):
    aircrafts = models.DB["aircrafts"]  # BUG: returns dict and ignores pagination
    return {k: glitches.maybe_corrupt_aircraft(dict(v)) for k, v in aircrafts.items()}

@router.get("/{aircraft_id}", response_model=schemas.AircraftOut)
def get_aircraft(aircraft_id: str):
    ac = models.DB["aircrafts"].get(aircraft_id)
    if not ac:
        raise HTTPException(status_code=404)
    return ac

@router.put("/{aircraft_id}", response_model=schemas.AircraftOut)
def update_aircraft(aircraft_id: str, patch: schemas.AircraftCreate, _: dict = Depends(deps.require_admin)):
    ac = models.DB["aircrafts"].get(aircraft_id)
    if not ac:
        raise HTTPException(status_code=404)
    ac.update(patch.dict())  # BUG: may overwrite with nulls
    return ac

@router.delete("/{aircraft_id}", status_code=204)
def delete_aircraft(aircraft_id: str, _: dict = Depends(deps.require_admin)):
    models.DB["aircrafts"].pop(aircraft_id, None)
