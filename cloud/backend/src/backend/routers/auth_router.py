from fastapi import APIRouter
from src.backend.models.token import Token
from src.backend.models.users import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from src.backend.services.auth_service import user_login, get_current_active_user
from typing import Annotated

router = APIRouter(prefix='/auth')

@router.post("/user-login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    response = await user_login(form_data) 
    return response

@router.get("/session", response_model=None)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
