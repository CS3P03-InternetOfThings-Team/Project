from typing import Annotated
from src.backend.database.auth_factory import parse_user_auth, store_auth_user
from src.backend.database.user_factory import get_all_users as get_all_users_factory, parse_user, store_user
from fastapi import Depends
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterFormBodyRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    
def build_user(user):
    user = user.dict()
    del user['id']
    return user 

async def get_all_users():
    users = await get_all_users_factory()
    built_users = [build_user(user) for user in users]
    return built_users

async def register_user(signup_data: RegisterFormBodyRequest):
    _id = ObjectId()
    email = EmailStr(signup_data.email)
    user_data = {
        "_id": _id,
        "name": signup_data.name,
        "enabled": True,
        "email": email
    }
    user = parse_user(user_data)
    stored_user = await store_user(user)
    hashed_password = str(pwd_context.hash(signup_data.password))
    auth_user_data = {
        "user_id": ObjectId(stored_user.inserted_id),
        "hashed_password": hashed_password
    }
    auth = parse_user_auth(auth_user_data)
    await store_auth_user(auth)
    return user
    