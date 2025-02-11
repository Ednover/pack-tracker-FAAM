from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.package import Package, Tracking
from .config import settings

client = AsyncIOMotorClient(settings.mongo_url)
database = client.get_database("pack_tracker")
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

async def create_package(package: Package):
    new_package = await collection.insert_one(package)
    created_package = await collection.find_one({'_id': new_package.inserted_id})
    return created_package

async def update_package(id: str, tracking: Tracking):
    package = await get_package_by_id(id)
    if not package:
        return None
    result = await collection.update_one({"_id": id}, {"$set": tracking.model_dump()})
    return result

async def delete_package(id: str):
    package = await get_package_by_id(id)
    if not package:
        return None
    result = await collection.delete_one({"_id": ObjectId(id)})
    print(result)
    return result