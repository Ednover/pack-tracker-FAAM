from datetime import datetime
from typing import Annotated, Optional, Text

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

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

class Receiver(BaseModel):
    name: str
    email: str

class Package(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    trackingID: str
    description: Text
    size: str
    tracking: Tracking
    receiver: Receiver
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

class CreatePackage(BaseModel):
    trackingID: str
    description: Text
    size: str
    tracking: Tracking
    receiver: Receiver
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class CreatePackageDTO(BaseModel):
    description: Text
    size: str
    receiver: Receiver
