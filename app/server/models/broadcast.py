from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from app.server.models.flow import FlowComponentOut
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


class BroadcastIn(BaseModel):
    flow: Optional[list[FlowComponentIn]]
    flowId: Optional[str]
    tags: list[str]
    exclude: list[str]
    sendToAll: Optional[bool] = Field(default_factory=False)
    platforms: Optional[list[str]]
    scheduled: Optional[bool] = Field(default_factory=False)
    sendAt: Optional[str]


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


class BroadcastHistorySchemaDbOut(BaseModel):
    id: str
    created_at: datetime
    created_by: PortalUserBasicSchemaOut
    flow_id: str
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
