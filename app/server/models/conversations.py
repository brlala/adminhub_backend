from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from app.server.models.message import MessageSchemaDb
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


class BotUserSchemaDb(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: Optional[str]
    gender: Optional[str]
    profile_pic_url: Optional[str]
    auth_flag: Optional[int]
    is_broadcast_subscribed: Optional[bool]
    last_active: BotUserSchemaLastActive
    bot_id: Optional[str]
    bot_user_group_id: Optional[str]
    platforms: list[str]
    facebook: Optional[BotUserSchemaFacebook]
    fullname: str


class ConversationBotUserSchema(BotUserSchemaDb):
    last_message: MessageSchemaDb

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GetConversationsTable(BaseModel):
    data: list[ConversationBotUserSchema]
    success: bool
    total: int
