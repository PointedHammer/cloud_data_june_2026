from typing import Optional
from fastapi import APIRouter, Body, Header, HTTPException, status  # type: ignore
from pydantic import BaseModel # type: ignore
import httpx

router = APIRouter()

class User(BaseModel):
    email: str
    address: Optional[str] = None

async def introspect(token: str) -> User:
    url = "0.0.0.0:80/introspect"
    headers = {
        "accept": "application/json",
        "auth": token
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    print(response)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return User(**response.json())

@router.get("/files")
async def Get(Auth: str = Header()) -> dict[str, str]:
    currrent_user = await introspect(Auth)
    return {"status": "ok"}

@router.post("/files")
async def post(Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}

@router.post("/merge")
async def merge_post(Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}

@router.get("/files/{id}")
async def get_by_id(id: int, Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}

@router.post("/files/{id}")
async def post_id(id: int, Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}

@router.delete("/files/{id}")
async def delete_id(id: int, Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}


