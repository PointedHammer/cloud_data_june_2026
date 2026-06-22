from fastapi import APIRouter
router = APIRouter()


@router.get("/")
async def healthcheck_get() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/")
async def healthcheck_post() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/{id}")
async def get_by_id(id: str) -> dict[str, str]:
    return {"status": "ok"}

@router.post("/id")
async def post_id() -> dict[str, str]:
    return {"status": "ok"}

@router.delete("/id")
async def delete_id() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/merge")
async def merge_post() -> dict[str, str]:
    return {"status": "ok"}

