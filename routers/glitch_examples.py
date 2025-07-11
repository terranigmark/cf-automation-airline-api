from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import time

router = APIRouter(prefix="/glitch-examples", tags=["Glitch Examples"])

@router.get("/success-but-error")
def success_but_error():
    """Return 200 with an error-like body."""
    return JSONResponse({"detail": "Error 400"}, status_code=200)

@router.get("/client-error")
def client_error():
    """Simulate a 4xx error."""
    raise HTTPException(status_code=400, detail="Simulated 4xx bug")

@router.get("/server-error")
def server_error():
    """Simulate a 5xx error."""
    raise HTTPException(status_code=500, detail="Simulated 5xx bug")

@router.get("/timeout")
def timeout_error():
    """Simulate a timeout leading to a 504 response."""
    time.sleep(2)
    raise HTTPException(status_code=504, detail="Simulated timeout")
