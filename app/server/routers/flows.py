from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from ..db_utils.flows import get_flow_one, get_flows_list, get_flows_filtered_field_list
from ..models.flow import FlowSchemaDbOut

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


@router.get("/", response_model=list[FlowSchemaDbOut])
async def get_flows():
    flows = await get_flows_list()
    return flows


@router.get("/fields")
async def get_flows(field: Optional[str] = None):
    flows = await get_flows_filtered_field_list(field)
    return flows


@router.post("/upload")
async def get_flows(field: Optional[str] = None):
    return {'url': 'https://placekitten.com/300/150'}



@router.get("/{flow_id}", response_model=FlowSchemaDbOut)
async def get_flow(flow_id: str):
    flow = await get_flow_one(flow_id)
    return flow


