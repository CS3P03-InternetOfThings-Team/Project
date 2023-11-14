from typing import Callable

from fastapi.routing import APIRoute
from fastapi import Request, Response

from backend.utils.middleware import validate_user_authorizarion_header



class TokenAuthMiddleware(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(primary_req: Request) -> Response:
            request = await validate_user_authorizarion_header(primary_req)
            response: Response = await original_route_handler(request)
            return response
        return custom_route_handler