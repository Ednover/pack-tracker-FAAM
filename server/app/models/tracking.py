from datetime import datetime
from pydantic import BaseModel

class History(BaseModel):
    location: str
    timestamp: datetime
    status: str

class UpdateTracking(BaseModel):
    location: str
    status: str

class Tracking(BaseModel):
    currentLocation: str
    currentStatus: str
    lastUpdate: datetime
    history: list[History]