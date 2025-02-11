
from fastapi import APIRouter, HTTPException, status

from datetime import datetime
from app.models.package import CreatePackage, History, Package, CreatePackageDTO, Tracking, UpdateTracking
from app.database import create_package, delete_package, get_all_packages, get_package_by_id, update_package

router = APIRouter()

@router.get("/packages")
async def get_packages():
    packages = await get_all_packages()
    return packages

@router.get("/packages/{package_id}", response_model=Package)
async def get_package(package_id: str):
    package = await get_package_by_id(package_id)
    if not package:
        raise HTTPException(404, "Package not found")
    return package

@router.post("/packages", response_model=Package, status_code=status.HTTP_201_CREATED)
async def save_package(package: CreatePackageDTO):
    print(package)
    trackingID: str = "12345" #generateTrackingId()
    tracking = Tracking (
      currentLocation="En el alamacén de Mérida",
      currentStatus="En preparación",
      lastUpdate=datetime.now(),
      history=[],
    )
    print(tracking)
    packageData = CreatePackage (
        trackingID=trackingID,
        description=package.description,
        size=package.size,
        tracking=tracking,
        receiver=package.receiver,
    )
    new_package = await create_package(packageData.model_dump())
    print(new_package)
    return new_package

@router.put("/packages/{package_id}", response_model=Package)
async def update_tracking(package_id: str, history: UpdateTracking):
    package: Package = await get_package_by_id(package_id)
    if not package:
        raise HTTPException(404, "Package not found")
    #cambiar el tracking (current) por el nuevo y pasarlo al final el current
    last_history = History(location=package.tracking.currentLocation, status=package.tracking.currentStatus, timestamp=package.tracking.lastUpdate)
    print(package)
    package.tracking.currentLocation = history.location
    package.tracking.currentStatus = history.status
    package.tracking.lastUpdate = datetime.now()
    package.tracking.history.append(last_history)
    updated_package = update_package(package_id, package)
    if not updated_package:
        raise HTTPException(404, "Error updating package")
    return update_package

@router.delete("/packages/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_package(package_id: str):
    response = await delete_package(package_id)
    if not response:
        raise HTTPException(404, "Package not found")
    return "Package deleted"
