from app.database import database
from app.models.user import User

collection = database.get_collection("users")

async def create_user(user: User):
    new_user = await collection.insert_one(user)
    created_user = await collection.find_one({ "_id": new_user.inserted_id })
    return created_user

async def get_user_by_username(username: str):
    user = await collection.find_one({ "username": username })
    return user