from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.server.models.pydantic_objectid import PyObjectId


class PortalUserSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    last_active: datetime
    force_change_password: bool
    password_history: list[str]
    invalid_login_attempts: int
    is_locked: bool
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    portal_user_group_id: Optional[PyObjectId]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    updated_by: Optional[PyObjectId]
    refresh_token_jti: str
    last_password_change: datetime
    #
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "_id": ObjectId("5efdc0a774f7e093ce73db73"),
    #             "first_name": "monitor",
    #             "last_name": "pand.ai",
    #             "username": "monitor pandai",
    #             "email": "monitor@pand.ai",
    #             "password": "pbkdf2:sha256:50000$jJRmI56N$8cfc063a63e7ee33af640494abfe20bd70610c920a7469839cabfd638d7b9b0c",
    #             "is_active": True,
    #             "portal_user_group_id": ObjectId("5efdc0a774f7e093ce73db72"),
    #             "created_at": datetime.utcnow(),
    #             "updated_at": datetime.utcnow(),
    #             "created_by": ObjectId("5efdc0a774f7e093ce73db73"),
    #             "updated_by": ObjectId("5efdc0a774f7e093ce73db73"),
    #             "invalid_login_attempts": 0,
    #             "is_locked": False,
    #             "refresh_token_jti": "3930088d-c380-4378-854c-bdb61eedd9dd",
    #             "last_active": datetime.utcnow()
    #         }
    #     }
    #     arbitrary_types_allowed = True
    #     json_encoders = {
    #         ObjectId: str
    #     }


class PortalUserBasicSchemaOut(BaseModel):
    id: str
    username: str
    avatar: Optional[str]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
