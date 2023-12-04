from pydantic import BaseModel
from bson.objectid import ObjectId

class Admin(BaseModel):
    user_id: ObjectId 

    class Config:
        arbitrary_types_allowed = True
    
