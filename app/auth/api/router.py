from email.header import Header
import token
from typing import Optional
import hashlib
import uuid
from fastapi import APIRouter, Body, Header, HTTPException, status  # type: ignore
from pydantic import BaseModel # type: ignore
from cryptography.hazmat.primitives import hashes

from app.auth.dependency_injection.domain.post_register import PostRegisterControllers
from app.auth.domain.services.computed_hashed_password_service import ComputeHashedPasswordService

router = APIRouter()

user_database = {}
token_database = {}

class user(BaseModel):
    email: str
    hashed_password: str
    address: Optional[str] = None

class RegisterInput(BaseModel):
    email: str
    password: str
    address: Optional[str] = None

class LoginInput(BaseModel):
    email: str
    password: str

post_login_controller = PostRegisterControllers.carlemany()

post_register_controller = PostRegisterControllers.carlemany()



compute_hashed_password_service = ComputeHashedPasswordService()

@router.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/register")
async def register(input : RegisterInput = Body()) -> dict[str, str]:
    post_register_controller(
        email = input.email, 
        password = input.password, 
        address = input.address)
    return {}

@router.post("/login")
async def post_login(input: LoginInput = Body()) -> str:
    generated_token = post_login_controller(
        email=input.email,
        password=input.password,
    )

    # Ensure a string is returned. Support several possible shapes of the controller result.
    if isinstance(generated_token, str):
        return generated_token
    if isinstance(generated_token, dict):
        for key in ("token", "access_token", "value"):
            if key in generated_token:
                return str(generated_token[key])
    for attr in ("token", "access_token", "value"):
        if hasattr(generated_token, attr):
            return str(getattr(generated_token, attr))

    # Fallback: stringify the object
    return str(generated_token)

@router.post("/logout")
async def logout(Auth: str = Header()) -> dict[str, str]:
    if token not in token_database:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    del(token_database[Auth])
    return {"status": "ok"}

class IntrospectOutput(BaseModel):
    email: str
    address: Optional[str] = None

@router.get("/introspect")
async def introspect(Auth: str = Header()) -> IntrospectOutput:
    if Auth not in token_database:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    email = token_database[Auth]
    user = user_database.get(email)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    return IntrospectOutput(email=user.email, address=user.address)

