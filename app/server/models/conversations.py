from datetime import datetime
from typing import Optional, Union

from pydantic.main import BaseModel

from app.server.models.bot_user import BotUserSchemaDb
from app.server.models.message import MessageSchemaDb, ConversationMessageDisplay
from app.server.utils.common import to_camel


class ConversationMessageUserSchema(BaseModel):
    convo_id: list[str]
    last_message_date: datetime
    user: BotUserSchemaDb
    fullname: Optional[str]
    convo_count: int

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ConversationBotUserSchema(BotUserSchemaDb):
    last_message: Optional[Union[MessageSchemaDb, ConversationMessageDisplay]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GetConversationsTable(BaseModel):
    data: list[ConversationBotUserSchema]
    success: bool
    total: int


class GetConversationsMessageTable(BaseModel):
    data: list[ConversationMessageUserSchema]
    success: bool
    total: int
