from typing import Optional

from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()

user_database = {}

class RegisterInput(BaseModel):
    email: str
    password: str
    address: Optional[str] = None

@router.get("")
async def register(input : RegisterInput = Body()) -> dict[str, str]:
    return {"status": "ok"}

@router.post("")
async def login() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/id")
async def logout() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/id")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/id")
async def introspect() -> dict[str, str]:
    return {"status": "ok"}

