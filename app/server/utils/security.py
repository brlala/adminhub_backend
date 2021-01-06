from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.env_variables import local_config
from app.server.db_utils.portal_user import get_portal_user
from app.server.models.current_user import CurrentUserSchema
from app.server.models.login import UserInDB, TokenData, User
from app.server.models.portal_user import PortalUserSchema

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/account")
app = FastAPI()


def verify_password(plain_password: str, hashed_password: str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


async def authenticate_user(username: str, password: str):
    user = await get_portal_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, local_config.JWT_SECRET_KEY, algorithm=local_config.JWT_ALGORITHM)
    return encoded_jwt


def check_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, local_config.JWT_SECRET_KEY, algorithms=[local_config.JWT_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        raise credentials_exception


async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUserSchema:
    try:
        payload = jwt.decode(token, local_config.JWT_SECRET_KEY, algorithms=[local_config.JWT_ALGORITHM])
        username: str = payload.get("username")
        print(payload)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_portal_user(username)
    # in case we want to disable a user immediately
    payload.update({"is_active": user.is_active})
    if user is None:
        raise credentials_exception
    return CurrentUserSchema(**payload)


async def get_current_active_user(current_user: CurrentUserSchema = Depends(get_current_user)) -> CurrentUserSchema:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
