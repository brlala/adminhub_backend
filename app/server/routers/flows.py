from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel

from ..db_utils.flows import get_flow_one, get_flows_filtered_field_list, get_flows_and_count_db, \
    add_flows_to_db_from_flow, remove_flow_db, edit_flow_db
from ..models.current_user import CurrentUserSchema
from ..models.flow import FlowSchemaDbOut, GetFlowsTable, FlowItemCreateIn, DeleteFlows, FlowItemEditIn, FlowResponse
from ..utils.security import get_current_active_user

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


@router.get("/", response_model=GetFlowsTable, response_model_exclude_none=True)
async def get_flows(flow_name: Optional[str] = Query(None, alias="name"),
                    created_at: Optional[datetime] = Query(None, alias="createdAt"),
                    updated_at: Optional[list[date]] = Query(None, alias="updatedAt"),
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
async def get_flows_filtered(field: Optional[str] = None, name: Optional[str] = None):
    flows = await get_flows_filtered_field_list(field, name)
    return flows


@router.get("/{flow_id}", response_model=FlowResponse, response_model_exclude_none=True)
async def get_flow(flow_id: str):
    if flow_id == 'undefined':
        return {'data': {}}
    flow = await get_flow_one(flow_id)
    return {'data': flow}


@router.post("/")
async def create_flow(flow: FlowItemCreateIn,
                      current_user: CurrentUserSchema = Depends(get_current_active_user)
                      ):
    # current_user = CurrentUserSchema(**{
    #         "username": "user@pand.ai",
    #         "userId": "5efdc63e74f7e093ce73db78",
    #         "access": "admin",
    #         "permissions": [
    #             "create_flow",
    #             "read_flow",
    #         ],
    #         "name": "Teh Li heng ",
    #         "email": "liheng@pand.ai",
    #         "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
    #         "is_active": True
    #     })
    status = await add_flows_to_db_from_flow(flow, current_user)
    result = {
        "status": status,
        "success": True,
    }
    return result


@router.delete("/")
async def delete_flow(flows: DeleteFlows, current_user: CurrentUserSchema = Depends(get_current_active_user)):
    status = await remove_flow_db(flows.key, current_user)
    result = {
        "status": status,
        "success": True,
    }
    return result


@router.put("/")
async def edit_flow(flow: FlowItemEditIn, current_user: CurrentUserSchema = Depends(get_current_active_user)):
    status = await edit_flow_db(flow, current_user)
    return {
        "status": status,
        "success": True,
    }
