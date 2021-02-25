from datetime import datetime
from typing import Optional, Union, Any

from pydantic import BaseModel

from app.server.models.flow import FlowComponentsOut, ButtonItemOut
from app.server.utils.common import to_camel


class MessageChatbot(BaseModel):
    convo_id: str
    flow_id: Optional[str]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ButtonItemConversationOut(ButtonItemOut):
    title: Optional[Union[str, dict]]


class FlowComponentsConversationOut(FlowComponentsOut):
    title: Optional[Any]
    subtitle: Optional[Any]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowComponentsConversationOut(FlowComponentsOut):
    title: Optional[Any]
    subtitle: Optional[Any]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MessageSchemaDb(BaseModel):
    id: str
    type: str
    data: FlowComponentsOut
    chatbot: MessageChatbot
    platform: str
    incoming_message_id: str
    sender_platform_id: str
    receiver_platform_id: str
    abbr: str
    sender_id: str
    receiver_id: str
    created_at: datetime

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
