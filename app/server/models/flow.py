from datetime import datetime
from enum import Enum
from typing import Optional

import stringcase
from pydantic import Field
from pydantic.main import BaseModel

from app.server.utils.common import to_camel


class FlowSchemaDb(BaseModel):
    id: str
    created_at: datetime
    created_by: Optional[str]
    updated_at: datetime
    updated_by: Optional[str]
    topic: Optional[str]
    is_active: bool
    name: Optional[str]
    flow: list[dict]
    type: str
    platforms: Optional[list[str]]
    params: Optional[list[str]]


class FlowSchemaDbOut(FlowSchemaDb):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GetFlowsTable(BaseModel):
    data: list[FlowSchemaDbOut]
    success: bool
    total: int


class FlowText(BaseModel):
    EN: Optional[str]


class FlowData(BaseModel):
    text: Optional[FlowText]


class AttachmentItem(BaseModel):
    file_name: str = Field(alias='fileName')
    url: str


class ButtonTypeEnum(str, Enum):
    url = 'web_url'
    flow = 'flow'


class ButtonItem(BaseModel):
    title: dict
    type: ButtonTypeEnum
    content: Optional[dict]
    url: Optional[str]


class QuickReplyItem(BaseModel):
    text: dict
    params: Optional[list[str]]
    payload: str = Field(alias='flowId')


class GenericTemplateItem(BaseModel):
    file_name: str = Field(alias='fileName')
    image_url: str = Field(alias='imageUrl')
    title: dict
    subtitle: dict
    buttons: list[ButtonItem]


class AttachmentItemComponent(BaseModel):  # include file, video, image component
    attachments: Optional[list[AttachmentItem]]


class GenericTemplateComponent(BaseModel):  # include file, video, image component
    elements: Optional[list[GenericTemplateItem]]


class QuickReplyComponent(BaseModel):  # include file, video, image component
    quick_replies: Optional[list[QuickReplyItem]] = Field(alias='quickReplies')


class TextComponent(BaseModel):  # include file, video, image component
    text: Optional[dict]


class FlowComponent(BaseModel):  # include file, video, image component
    flow_id: Optional[str] = Field(alias='flowId')
    params: Optional[list[str]]


class ButtonTemplateComponent(BaseModel):  # include file, video, image component
    text: Optional[dict]
    buttons: Optional[list[ButtonItem]]


class FlowComponents(AttachmentItemComponent, GenericTemplateComponent, TextComponent, FlowComponent,
                     ButtonTemplateComponent, QuickReplyComponent):
    pass


class FlowTypeEnum(str, Enum):
    GENERIC_TEMPLATE = 'genericTemplate'
    TEXT = 'text'
    IMAGE = 'imageAttachment'
    FILE = 'fileAttachment'
    BUTTON_TEMPLATE = 'buttonTemplate'
    FLOW = 'flow'
    MESSAGE = 'message'

    def __str__(self):
        if self.value == self.IMAGE:
            return 'images'
        elif self.value == self.FILE:
            return 'files'
        return stringcase.snakecase(self.value)


class FlowItem(BaseModel):
    type: FlowTypeEnum
    data: FlowComponents


class FlowItemCreateIn(BaseModel):
    name: str
    flow: list[FlowItem]


class NewFlow(BaseModel):
    topic: str
    type: str
    flow_items: list[dict]
