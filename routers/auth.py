from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import models, schemas, deps
import glitches

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=schemas.UserOut, status_code=201)
def signup(user_in: schemas.UserCreate):
    if any(u["email"] == user_in.email for u in models.DB["users"].values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    uid = models.generate_id("usr")
    user_dict = user_in.dict()
    user_dict["id"] = uid
    user_dict["password"] = deps.hash_password(user_in.password)
    user_dict["role"] = models.Role.passenger
    models.DB["users"][uid] = user_dict
    return glitches.maybe_corrupt_user(dict(user_dict))

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in models.DB["users"].values() if u["email"] == form.username), None)
    if not user or not deps.verify_password(form.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = deps.create_access_token({"sub": user["id"], "role": user["role"]})
    return schemas.Token(access_token=token)
