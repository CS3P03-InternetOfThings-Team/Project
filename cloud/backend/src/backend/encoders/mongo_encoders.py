from bson.objectid import ObjectId
from datetime import datetime
def json_encoder(obj):
    if isinstance(obj, ObjectId) or isinstance(obj, datetime):
        return str(obj) 
        
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
