from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.backend.services.user_service import get_all_users, register_user, RegisterFormBodyRequest
from src.backend.middlewares.admin_auth import AdminAuthMiddleware

router = APIRouter(prefix='/users', route_class=AdminAuthMiddleware)

@router.get("")
async def list_users_contoller():
    users = await get_all_users()
    json_compatible_item_data = jsonable_encoder(users)
    return JSONResponse(content=json_compatible_item_data)


@router.post("/register", response_model=None)
async def register_user_controller(body: RegisterFormBodyRequest):
    user = await register_user(body)
    return user
