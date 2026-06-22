from fastapi import FastAPI

app = FastAPI()

print("Modified file")

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/register")
async def register() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/login")
async def login() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/logout")
async def logout() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/introspect")
async def introspect() -> dict[str, str]:
    return {"status": "ok"}

