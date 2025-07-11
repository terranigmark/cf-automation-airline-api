from fastapi import APIRouter, Depends, HTTPException, status
import models, schemas, deps
import glitches

router = APIRouter(prefix="/users", tags=["Users"])

# Create user with chosen role (admin only)
@router.post("", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user_as_admin(
    user_in: schemas.UserCreateAdmin,
    _: dict = Depends(deps.require_admin),
):
    if any(u["email"] == user_in.email for u in models.DB["users"].values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    uid = models.generate_id("usr")
    user_dict = user_in.dict()
    user_dict["id"] = uid
    user_dict["password"] = deps.hash_password(user_in.password)
    models.DB["users"][uid] = user_dict
    return glitches.maybe_corrupt_user(dict(user_dict))

@router.get("", response_model=list[schemas.UserOut])
def list_users(p: dict = Depends(deps.pagination), _: dict = Depends(deps.require_admin)):
    users = list(models.DB["users"].values())[p["skip"]: p["skip"] + p["limit"]]
    return [glitches.maybe_corrupt_user(dict(u)) for u in users]

@router.get("/me", response_model=schemas.UserOut)
def me(user: dict = Depends(deps.get_current_user)):
    return glitches.maybe_corrupt_user(dict(user))

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: str, patch: schemas.UserCreate, current: dict = Depends(deps.get_current_user)):
    if current["id"] != user_id and current["role"] != models.Role.admin:
        raise HTTPException(status_code=403)
    user = models.DB["users"].get(user_id)
    if not user:
        raise HTTPException(status_code=404)
    user.update(patch.dict(exclude_unset=True))
    return glitches.maybe_corrupt_user(dict(user))

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, _: dict = Depends(deps.require_admin)):
    models.DB["users"].pop(user_id, None)
