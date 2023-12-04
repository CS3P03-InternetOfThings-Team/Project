from os import environ
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.backend.database.user_factory import get_user_by_filter
from src.backend.database.auth_factory import get_user_auth_by_user_id
from src.backend.models.token import Token
from src.backend.models.users import User
from src.backend.models.auth import Auth
from src.backend.models.token_data import TokenData
from src.backend.utils.exceptions import UnauthorizedException, BadRequestException


SECRET_KEY = environ["SECRET_KEY"]
ALGORITHM = environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], retrieve_id=False):
    credentials_exception = UnauthorizedException("Incorrect username or password", {"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub", None)
        print("email", email)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError as e:
        print(e)

        raise credentials_exception
    user = await get_user_by_filter({"email": token_data.email})
    if user is None:
        raise credentials_exception
    if not retrieve_id:
        delattr(user, "id")
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.enabled:
        raise BadRequestException("Inactive user")
    return current_user

async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UnauthorizedException("Incorrect username or password", {"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    data = {"access_token": access_token, "token_type": "bearer"}
    token_data = Token(**data)
    return token_data


async def authenticate_user(email: str, password: str):
    user = await get_user_by_filter({"email": email})
    if not user:
        return False

    user_id = str(user.id)
    user_auth = await get_user_auth_by_user_id(user_id)
    hashed_password = getattr(user_auth, 'hashed_password', None)
    if not hashed_password:
        return False
    if not verify_password(password, hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
