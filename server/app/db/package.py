from bson import ObjectId
from app.models.package import Package
from app.models.tracking import Tracking
from app.database import database

collection = database.get_collection("packages")

async def get_all_packages():
    packages = []
    cursor = collection.find({})
    async for document in cursor:
        packages.append(Package(**document))
    return packages

async def get_package_by_id(id: str):
    package = await collection.find_one({"_id": ObjectId(id)})
    return package

async def get_package_by_tracking_id(tracking_id: str):
    package = await collection.find_one({"trackingID": tracking_id})
    return package

async def create_package(package: Package):
    new_package = await collection.insert_one(package)
    created_package = await collection.find_one({'_id': new_package.inserted_id})
    return created_package

async def update_package(id: str, tracking: Tracking):
    await collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": {"tracking": tracking}}
    )
    updated_package = await collection.find_one({'_id': ObjectId(id)})
    return updated_package

async def delete_package(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    return result