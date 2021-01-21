from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ..db_utils.flows import get_flow_one, get_flows_filtered_field_list, get_flows_and_count_db
from ..models.flow import FlowSchemaDbOut, GetFlowsTable

router = APIRouter(
    tags=["flows"],
    prefix='/flows',
    responses={404: {"description": "Not found"}},
)


class CurrentUserParams(BaseModel):
    token: str

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZ…0OTJ9.rJ1WAF80i1EltnxAlfQI1PLJ9xrHH6qsw5Eeju9qB_w"
            }
        }


@router.get("/", response_model=GetFlowsTable)
async def get_flows(flow_name: Optional[str] = Query(None, alias="name"),
                    created_at: Optional[datetime] = Query(None, alias="createdAt"),
                    updated_at: Optional[list[datetime]] = Query(None, alias="updatedAt"),
                    current_page: int = Query(1, alias="current"), page_size: int = Query(20, alias="pageSize"),
                    triggered_counts: list[int] = Query(None, alias="triggeredCount"),
                    sort_by: str = Query(None, alias="sortBy"), language: str = 'EN'):
    flows, total = await get_flows_and_count_db(current_page=current_page, page_size=page_size,
                                                sorter=sort_by, flow_name=flow_name, language=language,
                                                updated_at=updated_at, triggered_counts=triggered_counts)

    result = {
        "data": flows,
        "success": True,
        "total": total
    }
    return result


@router.get("/fields")
async def get_flows(field: Optional[str] = None):
    flows = await get_flows_filtered_field_list(field)
    return flows


@router.get("/{flow_id}", response_model=FlowSchemaDbOut)
async def get_flow(flow_id: str):
    flow = await get_flow_one(flow_id)
    return flow
