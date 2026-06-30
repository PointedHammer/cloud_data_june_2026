from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Body, UploadFile, File  # type: ignore
from pydantic import BaseModel # type: ignore
import httpx  # type: ignore

router = APIRouter()
files_database = {}
id_counter = 0

class User(BaseModel):
    email: str
    address: Optional[str] = None

class FileBusinessObject(BaseModel):
    id: int
    user: User
    title: str
    path: Optional[str] = None

async def introspect(token: str) -> User:
    url = "http://0.0.0.0:80/introspect"
    headers = {
        "accept": "application/json",
        "auth": token
    }
    
    async with httpx.AsyncClient() as client:

            response = await client.get(url, headers=headers)

    print(response)

    if response.status_code != 200:

            raise HTTPException(

            status_code=401, detail="Unauthorized"

        )

    return User(**response.json())

class FilesPostInput(BaseModel):
    title: str
    author: str

@router.get("/files")
async def Get(Auth: str = Header(), input: FilesPostInput = Body()) -> int:
    current_user = await introspect(Auth)
    global id_counter
    current_id = id_counter
    id_counter += 1
    file = FileBusinessObject(id=current_id, 
                              user=current_user.email, 
                              title=input.title, 
                              author=input.author)
    files_database[current_id] = file
    return current_id


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
async def post_id(id: int, Auth: str = Header(), file_content: UploadFile = File()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}

@router.delete("/files/{id}")
async def delete_id(id: int, Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}


