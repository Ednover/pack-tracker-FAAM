from fastapi import FastAPI
from app.routers import admin, receiver, auth

app = FastAPI()

app.include_router(admin.router, prefix="/api/admin")
app.include_router(receiver.router, prefix="/api/receiver")
app.include_router(auth.router, prefix="/api/auth")

@app.get("/")
def read_root():
    return {"Hello": "World"}
