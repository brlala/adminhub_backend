from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

from app.server.models.flow import FlowItem, FlowItemOut
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


class BroadcastHistoryListSchemaDbOut(BaseModel):
    id: str
    created_by: PortalUserBasicSchemaOut
    send_at: datetime
    status: str
    tags: list[str]
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
    flow: list[FlowItemOut]
    send_at: datetime
    status: str
    tags: list[str]
    sent: int
    processed: int
    total: int
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
