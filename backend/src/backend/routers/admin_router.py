from fastapi import APIRouter

from src.backend.middlewares.admin_auth import AdminAuthMiddleware
from src.backend.routers.users_router import router

admin_router = APIRouter(prefix='/admin-management', route_class=AdminAuthMiddleware)
admin_router.include_router(router)
