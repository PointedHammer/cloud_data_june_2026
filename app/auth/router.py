from email.header import Header
import token
from typing import Optional
import hashlib
import uuid
from fastapi import APIRouter, Body, Header, HTTPException, status  # type: ignore
from pydantic import BaseModel # type: ignore

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

def compute_hash_password(email: str, password: str) -> str:
    hash_value = hashlib.sha256((email + password).encode()).hexdigest()
    return hash_value

@router.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/register")
async def register(input : RegisterInput = Body()) -> dict[str, str]:
    if input.email in user_database:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="User already exists")
    user_database[input.email] = user(
        email=input.email,
        hashed_password=compute_hash_password(input.email, input.password),
        address=input.address
    )
    return {"status": "ok"}

@router.post("/login")
async def login(input: LoginInput = Body()) -> dict[str, str]:
    if input.email not in user_database:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
    database_hashed_password = user_database[input.email].hashed_password
    hashed_password = compute_hash_password(input.email, input.password)
    if database_hashed_password != hashed_password:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    generated_token = str(uuid.uuid4())
    token_database[generated_token] = input.email

    return {"token": generated_token}

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

