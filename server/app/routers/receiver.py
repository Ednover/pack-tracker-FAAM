from fastapi import APIRouter, HTTPException

from app.db.package import get_package_by_tracking_id
from app.models.package import Package

router = APIRouter()

@router.get("/package/{tracking_id}", response_model=Package)
async def get_package_(tracking_id: str):
    package = await get_package_by_tracking_id(tracking_id)
    if not package:
        raise HTTPException(404, "Package not found")
    return package