from fastapi import APIRouter, Request, Query, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.backend.services.user_service import get_all_users, register_user, RegisterFormBodyRequest
from src.backend.middlewares.token_auth import TokenAuthMiddleware
from pydantic import BaseModel
from src.backend.models.users import User

router = APIRouter(prefix='/text-search', route_class=TokenAuthMiddleware)

@router.get("", response_model=None)
async def text_similariy_search(request:  Request):
    user: User | None = getattr(request.headers, "current_user", None)
    if not isinstance(user, User):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    params = request.query_params

    print("params", params)
    # results = collection.query(
    # query_texts=["This is a query document"],
    # n_results=2,
    # # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # # where_document={"$contains":"search_string"}  # optional filter
    # )  
    return "Done"
