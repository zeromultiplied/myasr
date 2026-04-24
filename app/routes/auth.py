import logging

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.db import create_user, get_user_by_id, get_user_by_username, update_user
from app.middleware.auth import create_access_token, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/auth")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UpdateProfileRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


@router.post("/register")
async def register(req: RegisterRequest):
    """Register a new user."""
    if len(req.username) < 2:
        raise HTTPException(400, "Username must be at least 2 characters")
    if len(req.password) < 4:
        raise HTTPException(400, "Password must be at least 4 characters")

    existing = get_user_by_username(req.username)
    if existing:
        raise HTTPException(400, "Username already exists")

    password_hash = hash_password(req.password)
    user_id = create_user(username=req.username, password_hash=password_hash)
    token = create_access_token({"sub": str(user_id)})
    logger.info("User registered: %s (id=%d)", req.username, user_id)
    return {"token": token, "user": {"id": user_id, "username": req.username}}


@router.post("/login")
async def login(req: LoginRequest):
    """Login and get a JWT token."""
    user = get_user_by_username(req.username)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(401, "Invalid username or password")

    token = create_access_token({"sub": str(user["id"])})
    return {"token": token, "user": {"id": user["id"], "username": user["username"], "email": user.get("email", "")}}


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Get current user profile."""
    return {"id": user["id"], "username": user["username"], "email": user.get("email", "")}


@router.put("/me")
async def update_me(req: UpdateProfileRequest, user: dict = Depends(get_current_user)):
    """Update current user profile."""
    updates = {}
    if req.username is not None:
        if len(req.username) < 2:
            raise HTTPException(400, "Username must be at least 2 characters")
        existing = get_user_by_username(req.username)
        if existing and existing["id"] != user["id"]:
            raise HTTPException(400, "Username already taken")
        updates["username"] = req.username
    if req.email is not None:
        updates["email"] = req.email
    if req.password is not None:
        if len(req.password) < 4:
            raise HTTPException(400, "Password must be at least 4 characters")
        updates["password_hash"] = hash_password(req.password)

    if updates:
        update_user(user["id"], **updates)

    updated = get_user_by_id(user["id"])
    return {"id": updated["id"], "username": updated["username"], "email": updated.get("email", "")}
