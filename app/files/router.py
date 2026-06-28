from fastapi import APIRouter
router = APIRouter()


@router.get("/files")
async def Get() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/files")
async def post() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/merge")
async def merge_post() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/files/{id}")
async def get_by_id(id: str) -> dict[str, str]:
    return {"status": "ok"}

@router.post("/files/{id}")
async def post_id(id: str) -> dict[str, str]:
    return {"status": "ok"}

@router.delete("/files/{id}")
async def delete_id(id: str) -> dict[str, str]:
    return {"status": "ok"}


