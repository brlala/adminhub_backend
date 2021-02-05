from typing import Optional

from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel

from ..db_utils.broadcasts import (get_broadcast_templates_list, get_broadcast_template_one, add_broadcast_template_db,
                                   validate_broadcast_template, update_broadcast_template_db,
                                   delete_broadcast_template_db, get_broadcast_history_list, get_broadcast_history_one,
                                   add_broadcast_db)
from ..models.broadcast import BroadcastTemplateSchemaDbOut, NewBroadcastTemplate, NewBroadcast
from app.server.models.current_user import CurrentUserSchema
from ..utils.security import get_current_active_user

router = APIRouter(
    tags=["broadcasts"],
    prefix='/broadcasts',
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


@router.get("/templates")
async def get_broadcast_templates(flow: Optional[list[str]] = Query(None),
                                  intersect: Optional[bool] = Query(None)
                                  ):
    broadcast_templates = await get_broadcast_templates_list(flow=flow, intersect=intersect)
    return {'data': broadcast_templates}


@router.post("/templates")
async def add_broadcast_template(broadcast_template: NewBroadcastTemplate,
                                 current_user: CurrentUserSchema = Depends(get_current_active_user)):
    validity, error_message = await validate_broadcast_template(broadcast_template)

    if not validity:
        raise HTTPException(status_code=400, detail=error_message)

    status = await add_broadcast_template_db(broadcast_template, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.get("/templates/{template_id}")
async def update_broadcast_template(template_id: str,
                                    current_user: CurrentUserSchema = Depends(get_current_active_user)):
    broadcast_template = await get_broadcast_template_one(template_id)
    return {'data': broadcast_template}


@router.put("/templates/{template_id}")
async def update_broadcast_template(template_id: str,
                                    broadcast_template: NewBroadcastTemplate,
                                    current_user: CurrentUserSchema = Depends(get_current_active_user)):
    validity, error_message = await validate_broadcast_template(broadcast_template, exclude=template_id)

    if not validity:
        raise HTTPException(status_code=400, detail=error_message)

    status = await update_broadcast_template_db(template_id, broadcast_template, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.delete("/templates/{template_id}")
async def delete_broadcast_template(template_id: str,
                                    current_user: CurrentUserSchema = Depends(get_current_active_user)):
    status = await delete_broadcast_template_db(template_id, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.get("/history")
async def get_broadcast_histories(tags: Optional[list[str]] = Query(None),
                                  intersect: Optional[bool] = Query(None),
                                  status: Optional[str] = Query(None),
                                  current_user: CurrentUserSchema = Depends(get_current_active_user)):
    broadcast_history = await get_broadcast_history_list(tags=tags, intersect=intersect, status=status)
    return {'data': broadcast_history}


@router.get("/history/{broadcast_id}")
async def get_broadcast_history(broadcast_id: str,
                                current_user: CurrentUserSchema = Depends(get_current_active_user)):
    broadcast = await get_broadcast_history_one(broadcast_id)
    return {'data': broadcast}


@router.get("/user-tags")
async def get_user_tags(current_user: CurrentUserSchema = Depends(get_current_active_user)):
    return {'data': ['Pandai', 'BBL', 'GELM']}


@router.post("/send")
async def get_user_tags(broadcast: NewBroadcast,
                        current_user: CurrentUserSchema = Depends(get_current_active_user)):

    status = await add_broadcast_db(broadcast, current_user)
    return {
        "status": status,
        "success": True,
    }


