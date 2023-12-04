from motor import motor_asyncio
import os

from bson.objectid import ObjectId
from typing import Mapping, Any

from src.backend.models.auth import Auth


client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
mongo_db = client.get_database(os.environ["MONGODB_DATABASE"])
auth_collection = mongo_db.get_collection("auth")

def parse_user_auth(user_data: Mapping[str, Any]) -> Auth: 
    return Auth.parse_obj(user_data)

async def get_user_auth_by_user_id(id_: str):
    user_auth = await auth_collection.find_one({"user_id": ObjectId(id_)})
    if user_auth is None:
        return None
    return parse_user_auth(user_auth)

async def store_auth_user(auth_user: Auth):    
    response = await auth_collection.insert_one(auth_user.dict())
    return response