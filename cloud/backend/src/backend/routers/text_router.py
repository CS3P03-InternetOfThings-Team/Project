from fastapi import APIRouter, Request, Query, HTTPException, status, Header
from fastapi.responses import JSONResponse
import uuid
import numpy as np

from fastapi.encoders import jsonable_encoder
from src.backend.services.user_service import get_all_users, register_user, RegisterFormBodyRequest
from src.backend.middlewares.token_auth import TokenAuthMiddleware
from pydantic import BaseModel
from src.backend.models.users import User
# from functools import reduce

from chromadb import Client
client = Client()
collection = client.create_collection("all-my-documents")
# https://www.trychroma.com/

router = APIRouter(prefix='/text', route_class=TokenAuthMiddleware)

class NewDataBodyRequest(BaseModel):
    text: str
    timestamp: str
    username: str #email
 

@router.post("/store-text", response_model=None)
async def store_text(request: Request, body: NewDataBodyRequest):
    user: User | None = getattr(request.headers, "current_user", None)
    if not isinstance(user, User):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    myuuid = uuid.uuid4()
    collection.add(
    documents=[body.text], # we embed for you, or bring your own
    metadatas=[{"source": "Raspberry Pi", "timestamp": body.timestamp, "username": body.username}], # filter on arbitrary metadata!
    ids=[str(myuuid)], # must be unique for each doc 
    )
    return {"message": "Done"}


@router.get("/get-texts", response_model=None)
async def text_similariy_search(
    request: Request, 
    text: str = Query(..., title="Texto de búsqueda", description="Texto no puede ser nulo"),
    limit: int = Query(3, title="Número de resultados", gt=0, le=100),
    ):
    user: User | None = getattr(request.headers, "current_user", None)
    if not isinstance(user, User):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    params = request.query_params
    limit = int(params.get("limit", 5))
    results = collection.query(
        query_texts=[text],
        n_results=10,
        where={"username": user.email}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )  
    response = list()
    ids = np.matrix(results['ids']).flatten().tolist()[0]
    texts = np.matrix(results['documents']).flatten().tolist()[0]
    metadatas = np.matrix(results['metadatas']).flatten().tolist()[0] 
    for i in range(min(limit, len(ids))):
        item = {
            "uuid": ids[i],
            "text": texts[i],
            "metadata": metadatas[i]
        }
        response.append(item)

    return response

