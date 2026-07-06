from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.files.database import models
from app.auth.api.router import router as auth_router
from app.files.config import DATABASE_URL
from app.files.router import router as files_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(files_router)

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

register_tortoise(

    app,

    db_url=DATABASE_URL,

    modules={"models": models},

    generate_schemas=False,

    add_exception_handlers=True,

)