from pydantic import BaseModel, EmailStr, Field, StrictBool
from bson.objectid import ObjectId
from bson import ObjectId

class User(BaseModel):
    id: ObjectId = Field(..., alias="_id")  
    name: str = Field()
    email: EmailStr = Field()
    enabled: StrictBool = Field()

    class Config:
        arbitrary_types_allowed = True