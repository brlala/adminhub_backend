from datetime import timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from app.server.db_utils.portal_user_group import get_user_permissions
from app.server.utils.security import authenticate_user, create_access_token
from app.env_variables import local_config

router = APIRouter(
    tags=["security"],
    responses={404: {"description": "Not found"}},
)


class LoginParams(BaseModel):
    username: str
    password: str
    autoLogin: bool
    type: str

    class Config:
        schema_extra = {
            "example": {
                "username": "user@pand.ai",
                "password": "mysecret",
                "autoLogin": True,
                "type": "account"
            }
        }


class CurrentUserParams(BaseModel):
    token: str

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZ…0OTJ9.rJ1WAF80i1EltnxAlfQI1PLJ9xrHH6qsw5Eeju9qB_w"
            }
        }


@router.post("/login/account")
async def login_for_access_token(data: LoginParams):
    user = await authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=local_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    user_permissions = await get_user_permissions(user.portal_user_group_id)
    jwt_data = {
        "username": user.username,
        "userId": str(user.id),
        "access": user_permissions['access'],
        "permissions": user_permissions['permissions'],
        "name": f"{user.first_name} {user.last_name}",
        "email": user.email,
        "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png"
    }
    access_token = create_access_token(
        data=jwt_data, expires_delta=access_token_expires)
    return {"access_token": access_token,
            "token_type": "bearer",
            "status": "ok",
            "type": data.type,
            "currentAuthority": 'admin'}


# @router.get("/currentUser")
# async def get_current_user(data: CurrentUserParams):
#     user = await authenticate_user(data.username, data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=local_config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
#     permissions = await get_user_permissions(user['portal_user_group_id'])
#     access_token = create_access_token(
#         data={"username": user['username'], "id": str(user['_id']), "role": permissions['role'],
#               "permissions": permissions['access']}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer", "status": "ok", "type": data.type,
#             "currentAuthority": 'admin'}
