from pydantic import BaseModel, Field

from src.backend.database.user_factory import get_user_by_id
from bson.objectid import ObjectId

class Auth(BaseModel):
    user_id: ObjectId 
    hashed_password: str = Field(...)

    # @validator("user_id")
    # async def validate_user_id(cls, value):
    #     user_id_str = str(value)
    #     user = await get_user_by_id(user_id_str)
    #     if not user:
    #         raise ValueError("El user_id no existe en la colección de users")
    #     return value
    class Config:
        arbitrary_types_allowed = True
    
