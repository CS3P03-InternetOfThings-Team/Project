from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.backend.services.user_service import get_all_users, register_user, RegisterFormBodyRequest
from src.backend.middlewares.admin_auth import AdminAuthMiddleware
from pydantic import BaseModel

router = APIRouter(prefix='/users', route_class=AdminAuthMiddleware)

@router.get("")
async def list_users_contoller():
    users = await get_all_users()
    json_compatible_item_data = jsonable_encoder(users)
    return JSONResponse(content=json_compatible_item_data)


class RegisterResponseBody(BaseModel):
    email: str
    name: str
    enabled: bool

@router.post("/register", response_model=RegisterResponseBody)
async def register_user_controller(body: RegisterFormBodyRequest):
    user = await register_user(body)
    return user
