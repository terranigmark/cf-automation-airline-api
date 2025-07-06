from fastapi import APIRouter, Depends, HTTPException
import models, schemas, deps

router = APIRouter(prefix="/airports", tags=["Airports"])

@router.post("", response_model=schemas.AirportOut, status_code=201)
def create_airport(airport: schemas.AirportCreate, _: dict = Depends(deps.require_admin)):
    if airport.iata_code in models.DB["airports"]:
        raise HTTPException(status_code=400, detail="Airport exists")
    models.DB["airports"][airport.iata_code] = airport.dict()
    return airport

@router.get("", response_model=list[schemas.AirportOut])
def list_airports(p: dict = Depends(deps.pagination)):
    airports = list(models.DB["airports"].values())[p["skip"]:p["skip"]+p["limit"]]
    return airports

@router.get("/{iata_code}", response_model=schemas.AirportOut)
def get_airport(iata_code: str):
    ap = models.DB["airports"].get(iata_code)
    if not ap:
        raise HTTPException(status_code=404)
    return ap

@router.put("/{iata_code}", response_model=schemas.AirportOut)
def update_airport(iata_code: str, patch: schemas.AirportCreate, _: dict = Depends(deps.require_admin)):
    if iata_code not in models.DB["airports"]:
        raise HTTPException(status_code=404)
    models.DB["airports"][iata_code].update(patch.dict())
    return models.DB["airports"][iata_code]

@router.delete("/{iata_code}", status_code=204)
def delete_airport(iata_code: str, _: dict = Depends(deps.require_admin)):
    models.DB["airports"].pop(iata_code, None)
