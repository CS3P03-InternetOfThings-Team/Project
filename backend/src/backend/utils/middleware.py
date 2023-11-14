from fastapi import Request

from src.backend.services.auth_service import get_current_user
from src.backend.models.users import User
from src.backend.utils.exceptions import UnauthorizedException, InternalServerException
from src.backend.database.admins_factory import get_admin_by_user_id

def get_unauthorized_exception():
    credentials_exception = UnauthorizedException(
        "Could not validate credentials", 
        {"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception


async def validate_user_authorizarion_header(request: Request) -> Request: 
    authorization = request.headers.get('Authorization', None) or ""
    if authorization is None:
        raise get_unauthorized_exception()
    token_bearer = authorization.split(" ")
    if len(token_bearer) != 2:
        raise get_unauthorized_exception()
    token = token_bearer[1]
    current_user = await get_current_user(token, True)
    setattr(request.headers, "current_user", current_user)
    return request

async def validate_current_user_id_admin(request: Request) -> Request: 
    user: User | None = getattr(request.headers, "current_user", None)
    if not isinstance(user, User):
        print("Set current_user to request headers")
        raise InternalServerException("Internal Server Error")

    is_user_admin = bool(await get_admin_by_user_id(user.id))
    if not is_user_admin:
        raise get_unauthorized_exception()

    return request