from fastapi import APIRouter, Query

from fastapi import APIRouter, Query

from ..db_utils.bot_user import get_bot_user_db, update_bot_user_db
from ..db_utils.conversations import get_user_message_conversations_and_count_db, get_convo_conversations_and_count_db
from ..models.bot_user import BotUserSchemaDb
from ..models.message import GetMessagesTable

router = APIRouter(
    tags=["Bot User"],
    prefix="/botuser",
    responses={404: {"description": "Not found"}},
)


@router.get("/{bot_user_id}", response_model_exclude_none=True, response_model=BotUserSchemaDb)
async def get_bot_user(bot_user_id: str):
    return await get_bot_user_db(bot_user_id)


@router.put("/{bot_user_id}")
async def update_bot_user(bot_user_id: str, tags: list[str] = Query([])):
    status = await update_bot_user_db(bot_user_id, tags=tags)
    return {
        "status": status,
        "success": True,
    }
