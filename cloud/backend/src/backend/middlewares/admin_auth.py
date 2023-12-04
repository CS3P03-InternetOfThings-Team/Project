from typing import Callable

from fastapi.routing import APIRoute
from fastapi import Request, Response

from src.backend.utils.middleware import validate_user_authorizarion_header, validate_current_user_id_admin

class AdminAuthMiddleware(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def admin_route_handler(primary_req: Request) -> Response:
            validated_req: Request = await validate_user_authorizarion_header(primary_req)
            validate_admin_user: Request = await validate_current_user_id_admin(validated_req)
            response: Response = await original_route_handler(validate_admin_user)
            return response
        return admin_route_handler