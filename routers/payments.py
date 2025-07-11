from fastapi import APIRouter, Depends, HTTPException, status
import models, schemas, deps
import glitches

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("", response_model=schemas.PaymentOut, status_code=status.HTTP_201_CREATED)
def pay(pay: schemas.PaymentCreate, user: dict = Depends(deps.get_current_user)):
    bug = glitches.maybe_bug()
    if bug:
        return bug
    bk = models.DB["bookings"].get(pay.booking_id)
    if not bk:
        raise HTTPException(status_code=404, detail="Booking not found")
    if bk["user_id"] != user["id"]:
        raise HTTPException(status_code=403)
    if bk["status"] != models.BookingStatus.draft:
        raise HTTPException(status_code=400, detail="Booking already paid/cancelled")
    pid = models.generate_id("pay")
    models.DB["payments"][pid] = {
        "id": pid,
        "booking_id": pay.booking_id,
        "status": models.PaymentStatus.success,  # simplified mock
    }
    bk["status"] = models.BookingStatus.paid
    return glitches.maybe_corrupt_payment(models.DB["payments"][pid])

@router.get("/{payment_id}", response_model=schemas.PaymentOut)
def get_payment(payment_id: str, user: dict = Depends(deps.get_current_user)):
    payment = models.DB["payments"].get(payment_id)
    if not payment:
        raise HTTPException(status_code=404)
    bk = models.DB["bookings"].get(payment["booking_id"])
    if user["role"] != models.Role.admin and bk["user_id"] != user["id"]:
        raise HTTPException(status_code=403)
    return glitches.maybe_corrupt_payment(dict(payment))
