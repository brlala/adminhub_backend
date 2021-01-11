from fastapi import APIRouter
from fastapi import Depends

from app.server.models.current_user import CurrentUserSchema
from app.server.models.login import User
from app.server.utils.security import get_current_active_user

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me/", tags=["users"])
async def read_users_me(current_user: CurrentUserSchema = Depends(get_current_active_user)):
    return current_user


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


# @router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)
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
#               "permissions": permissions['access']}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}





@router.get("/users/me/items/", tags=["users"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
