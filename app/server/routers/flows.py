from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ..db_utils.flows import get_flow_from_db
from ..models.flow import FlowSchemaDbOut

router = APIRouter(
    tags=["flows"],
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


@router.get("/flow/{flow_id}", response_model=FlowSchemaDbOut)
async def get_flow(flow_id: str):
    flow = await get_flow_from_db(flow_id)
    return flow
