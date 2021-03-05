from fastapi import APIRouter, Query

from ..db_utils.bot_user import get_bot_user_db, update_bot_user_db
from ..models.bot_user import BotUserSchemaDb

router = APIRouter(
    tags=["Bot User"],
    prefix="/botuser",
    responses={404: {"description": "Not found"}},
)


@router.get("/{bot_user_id}", response_model_exclude_none=True, response_model=BotUserSchemaDb)
async def get_bot_user(bot_user_id: str):
    return await get_bot_user_db(bot_user_id)


@router.patch("/{bot_user_id}")
async def update_bot_user(bot_user_id: str, tags: list[str] = Query([])):
    status = await update_bot_user_db(bot_user_id, tags=tags)
    return {
        "status": status,
        "success": True,
    }
