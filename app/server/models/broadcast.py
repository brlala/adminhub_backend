from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from app.server.models.flow import FlowItem, FlowItemOut, NewFlow
from app.server.models.portal_user import PortalUserBasicSchemaOut
from app.server.utils.common import to_camel


class BroadcastTemplateSchemaDb(BaseModel):
    id: str
    created_at: datetime
    created_by: Optional[str]
    updated_at: datetime
    updated_by: Optional[str]
    flow: list[str]
    is_active: bool
    name: Optional[str]
    platforms: Optional[list[str]]


class BroadcastTemplateSchemaDbOut(BroadcastTemplateSchemaDb):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GetBroadcastTemplatesTable(BaseModel):
    data: list[BroadcastTemplateSchemaDbOut]
    success: bool
    total: int


class NewBroadcastTemplate(BaseModel):
    name: str
    flow: list[str]
    platforms: Optional[list[str]]


class FlowTextIn(BaseModel):
    EN: Optional[str]


class FlowButtonsIn(BaseModel):
    title: Optional[FlowTextIn]
    type: Optional[str]
    url: Optional[str]
    flow_id: Optional[str] = Field(alias='flowId')


class FlowElementsIn(BaseModel):
    title: Optional[FlowTextIn]
    subtitle: Optional[FlowTextIn]
    image_url: Optional[str] = Field(alias='imageUrl')
    buttons: Optional[list[FlowButtonsIn]]


class FlowDataIn(BaseModel):
    text: Optional[FlowTextIn]
    url: Optional[str]
    title: Optional[FlowTextIn]
    buttons: Optional[list[FlowButtonsIn]]
    elements: Optional[list[FlowElementsIn]]


class FlowComponentIn(BaseModel):
    type: str
    data: FlowDataIn


class NewBroadcast(BaseModel):
    flow: list[FlowComponentIn]
    tags: list[str]
    exclude: list[str]
    sendToAll: bool = Field(default_factory=False)
    platforms: Optional[list[str]]


class BroadcastHistoryListSchemaDbOut(BaseModel):
    id: str
    created_by: PortalUserBasicSchemaOut
    send_at: datetime
    status: str
    tags: list[str]
    exclude: list[str]
    send_to_all: bool
    sent: int
    processed: int
    total: int
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowTextOut(BaseModel):
    EN: Optional[str]


class FlowButtonsOut(BaseModel):
    title: Optional[FlowTextOut]
    type: Optional[str]
    url: Optional[str]
    flow_id: Optional[str]
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowElementsOut(BaseModel):
    title: Optional[FlowTextOut]
    subtitle: Optional[FlowTextOut]
    image_url: Optional[str]
    buttons: Optional[list[FlowButtonsOut]]
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowDataOut(BaseModel):
    text: Optional[FlowTextOut]
    url: Optional[str]
    title: Optional[FlowTextOut]
    buttons: Optional[list[FlowButtonsOut]]
    elements: Optional[list[FlowElementsOut]]
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowComponentOut(BaseModel):
    type: str
    data: FlowDataOut
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class BroadcastHistorySchemaDbOut(BaseModel):
    id: str
    created_at: datetime
    created_by: PortalUserBasicSchemaOut
    flow: list[FlowComponentOut]
    send_at: datetime
    status: str
    tags: list[str]
    exclude: list[str]
    send_to_all: bool
    sent: int
    processed: int
    total: int
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
