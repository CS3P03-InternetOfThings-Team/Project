from motor import motor_asyncio
import os

from bson.objectid import ObjectId
from typing import Mapping, Any

from src.backend.models.admin import Admin

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
mongo_db = client.get_database(os.environ["MONGODB_DATABASE"])
admin_collection = mongo_db.get_collection("admins")

def parse_user_auth(user_data: Mapping[str, Any]) -> Admin: 
    return Admin.parse_obj(user_data)

async def get_admin_by_user_id(id_: ObjectId):
    user_auth = await admin_collection.find_one({"user_id": id_})
    if user_auth is None:
        return None
    return parse_user_auth(user_auth)
