from fastapi import FastAPI
from app.routers import admin

app = FastAPI()

app.include_router(admin.router, prefix="/api/admin")

@app.get("/")
def read_root():
    return {"Hello": "World"}
