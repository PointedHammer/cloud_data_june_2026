from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Body, UploadFile, File, status  # type: ignore
from pydantic import BaseModel # type: ignore
import importlib
from pypdf import PdfMerger  # type: ignore
import httpx  # type: ignore
import uuid

try:
    PDFMerger = importlib.import_module("pypdf").PDFMerger
except ModuleNotFoundError:
    PDFMerger = None


router = APIRouter()
files_database = {}
id_counter = 0

class User(BaseModel):
    email: str
    address: Optional[str] = None

class FileBusinessObject(BaseModel):
    id: int
    user_id: str
    title: str
    author: str
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

async def get_file(user_id : str, file_id: int) -> FileBusinessObject:
     if file_id >= id_counter or file_id < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
     current_file = files_database[file_id]
     if current_file.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
     return current_file
     

class FilesPostInput(BaseModel):
    title: str
    author: str

@router.post("/files")
async def post_files(Auth: str = Header(), input: FilesPostInput = Body()) -> int:
    current_user = await introspect(Auth)
    global id_counter
    current_id = id_counter
    id_counter += 1
    file = FileBusinessObject(id=current_id, 
                              user_id=current_user.email, 
                              title=input.title, 
                              author=input.author)
    files_database[current_id] = file
    return current_id


@router.post("/files")
async def post(Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}

class PostFilesMerge(BaseModel):
    file1_id: int
    file2_id: int    

@router.post("/merge")
async def merge_post(Auth: str = Header(), input: PostFilesMerge = Body()) -> int:
    current_user = await introspect(Auth)
    global id_counter
    current_file1 : FileBusinessObject = await get_file(current_user.email, input.file1_id)
    current_file2 : FileBusinessObject = await get_file(current_user.email, input.file2_id)
    if current_file1.path is None or current_file2.path is None:
        raise HTTPException(status_code=status.BAD_REQUEST, detail="Both files must have content to merge.")
    file_path_1 = current_file1.path

    file_path_2 = current_file2.path

    pdfs = [file_path_1, file_path_2]

    merger = PdfMerger()

    for pdf in pdfs:

        merger.append(pdf)

    merged_name = "files/" + current_file1.title + "_" + current_file2.title + ".pdf"

    merger.write(merged_name)

    merger.close()

    merged_file = FileBusinessObject(
        id=id_counter,
        user_id=current_user.email,
        title=f"{current_file1.title}_{current_file2.title}",
        author=f"{current_file1.author}_{current_file2.author}",
        path=merged_name
    )
    files_database[id_counter] = merged_file
    id_counter += 1
    return merged_file.id

class FilesIdGetOutput(BaseModel):
    title: str
    author: str

@router.get("/files/{id}")
async def get_by_id(id: int, Auth: str = Header()) -> FilesIdGetOutput:

    current_user = await introspect(Auth)
    current_file : FileBusinessObject = await get_file(current_user.email, id)
    return FilesIdGetOutput(title=current_file.title, author=current_file.author)

@router.post("/files/{id}")
async def post_id(id: int, Auth: str = Header(), file_content: UploadFile = File()) -> dict[str, str]:
    current_user = await introspect(Auth)
    current_file = await get_file(current_user.email, id)
    filename = str(uuid.uuid4())
    prefix = "app/files/"
    with open(prefix + filename + ".pdf", "wb") as buffer:
        while chunk := await file_content.read(8192):
            buffer.write(chunk)
    current_file.path = prefix + filename + ".pdf"
    return {}

@router.delete("/files/{id}")
async def delete_id(id: int, Auth: str = Header()) -> dict[str, str]:
    current_user = await introspect(Auth)
    return {"status": "ok"}


