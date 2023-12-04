from motor import motor_asyncio
import os

from bson.objectid import ObjectId
from typing import Mapping, Any

from src.backend.models.users import User

from dotenv import load_dotenv
load_dotenv(".backend.env")

client = motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
mongo_db = client.get_database(os.environ["MONGODB_DATABASE"])
user_collection = mongo_db.get_collection("users")


def parse_user(user_data: Mapping[str, Any]) -> User:
    """
    Parse a user from a MongoDB document.

    :param user_data: The MongoDB document.
    :return: The parsed user.
    :raises ValidationError: If the user data is invalid 
    """
    return User.parse_obj(user_data)


async def store_user(user: User):
    response = await user_collection.insert_one(user.dict())
    return response

async def get_all_users() -> list[User]:
    """
    Get all users from the database.
    
    :return: A list of all users.
    :raises ValidationError: If any of the user data in the db is invalid
    """
    users_data = user_collection.find()
    return [parse_user(user_data) async for user_data in users_data]


async def get_user_by_id(id: str) -> User | None:
    """
    Get a user by their ID.

    :param id: The ID of the user.
    :return: The user with the given ID, or None if no such user exists.
    :raises ValidationError: If the user data in the db is invalid
    """

    user_document = await user_collection.find_one({"_id": ObjectId(id)})
    if user_document is None:
        return None
    return parse_user(user_document)

async def get_user_by_filter(filter_: dict) -> User | None:
    """
    Get a user by custom filter.

    :param filter: The custom filter.
    :return: The user with the given filter, or None if no such user exists.
    :raises ValidationError: If the user data in the db is invalid
    """

    user_document = await user_collection.find_one(filter_)
    if user_document is None:
        return None
    return parse_user(user_document)
