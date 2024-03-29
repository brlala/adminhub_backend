from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from app.server.utils.common import to_camel


class BotUserSchemaLastActive(BaseModel):
    received_at: datetime
    received_message_id: str
    sent_at: datetime
    sent_message_id: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BotUserSchemaFacebook(BaseModel):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BotUserSchemaChatbot(BaseModel):
    registration_date: Optional[datetime] = None
    note: str = ''

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BotUserSchemaDb(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: Optional[str]
    gender: Optional[str]
    profile_pic_url: Optional[str]
    auth_flag: Optional[int]
    is_broadcast_subscribed: Optional[bool]
    last_active: Optional[BotUserSchemaLastActive]
    bot_id: Optional[str]
    bot_user_group_id: Optional[str]
    platforms: list[str]
    facebook: Optional[BotUserSchemaFacebook]
    fullname: Optional[str]
    tags: list[str] = []
    chatbot: Optional[BotUserSchemaChatbot] = None

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BotUserBasicSchemaDb(BaseModel):
    id: str
    name: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BotUserUpdateModel(BaseModel):
    tags: Optional[list[str]]
    note: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "tags": [
                    "Tester",
                    "Staff"
                ],
                "note": "2"
            }
        }
