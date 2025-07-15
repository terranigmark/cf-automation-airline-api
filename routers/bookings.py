from fastapi import APIRouter, Depends, HTTPException, status
import models, schemas, deps
import glitches

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("", response_model=schemas.BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(bk: schemas.BookingCreate, user: dict = Depends(deps.get_current_user)):
    bug = glitches.maybe_bug()
    if bug:
        return bug
    flight = models.DB["flights"].get(bk.flight_id)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    bid = models.generate_id("bkg")
    data = bk.dict()
    data |= {"id": bid, "user_id": user["id"], "status": models.BookingStatus.draft}
    models.DB["bookings"][bid] = data
    return data

@router.get("", response_model=list[schemas.BookingOut])
def list_bookings(p: dict = Depends(deps.pagination), user: dict = Depends(deps.get_current_user)):
    items = models.DB["bookings"].values()
    if user["role"] != models.Role.admin:
        items = [b for b in items if b["user_id"] == user["id"]]
    items = list(items)[p["skip"]:p["skip"]+p["limit"]]
    return items

@router.get("/{booking_id}", response_model=schemas.BookingOut)
def get_booking(booking_id: str, user: dict = Depends(deps.get_current_user)):
    bk = models.DB["bookings"].get(booking_id)
    if not bk:
        raise HTTPException(status_code=404)
    if user["role"] != models.Role.admin and bk["user_id"] != user["id"]:
        raise HTTPException(status_code=403)
    return glitches.maybe_corrupt_booking(dict(bk))

@router.patch("/{booking_id}", response_model=schemas.BookingOut)
def update_booking(booking_id: str, patch: dict, user: dict = Depends(deps.get_current_user)):
    bk = models.DB["bookings"].get(booking_id)
    if not bk:
        raise HTTPException(status_code=404)
    if bk["status"] != models.BookingStatus.draft:
        raise HTTPException(status_code=400, detail="Only draft bookings can be edited")
    if bk["user_id"] != user["id"]:
        raise HTTPException(status_code=403)
    bk.update(patch)
    return bk

@router.delete("/{booking_id}", status_code=204)
def cancel_booking(booking_id: str, user: dict = Depends(deps.get_current_user)):
    bk = models.DB["bookings"].get(booking_id)
    if not bk:
        raise HTTPException(status_code=404)
    if bk["user_id"] != user["id"] and user["role"] != models.Role.admin:
        raise HTTPException(status_code=403)
    bk["status"] = models.BookingStatus.cancelled
