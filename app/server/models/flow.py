from datetime import datetime
from typing import Optional

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


class AttachmentItem(BaseModel):
    fileName: str
    url: str


class ButtonItem(BaseModel):
    title: dict
    type: str
    content: dict


class GenericTemplateItem(BaseModel):
    fileName: str
    imageUrl: str
    title: dict
    subtitle: dict
    buttons: list[ButtonItem]


class AttachmentItemComponent(BaseModel):  # include file, video, image component
    attachments: Optional[list[AttachmentItem]]


class GenericTemplateComponent(BaseModel):  # include file, video, image component
    elements: Optional[list[GenericTemplateItem]]


class TextComponent(BaseModel):  # include file, video, image component
    text: Optional[dict]


class FlowComponent(BaseModel):  # include file, video, image component
    flowId: Optional[str]
    params: Optional[list[str]]


class ButtonTemplateComponent(BaseModel):  # include file, video, image component
    text: Optional[dict]
    buttons: Optional[list[ButtonItem]]


class FlowComponents(AttachmentItemComponent, GenericTemplateComponent, TextComponent, FlowComponent,
                     ButtonTemplateComponent):
    pass


class FlowItem(BaseModel):
    type: str
    data: FlowComponents


class FlowItemCreateIn(BaseModel):
    name: str
    flow: list[FlowItem]


class NewFlow(BaseModel):
    topic: str
    type: str
    flow_items: list[dict]
