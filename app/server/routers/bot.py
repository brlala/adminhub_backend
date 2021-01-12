from fastapi import APIRouter

from ..db_utils.bot import get_bot_db
from ..models.bot import BotSchemaDbOut
from app.server.core.env_variables import local_config

router = APIRouter(
    tags=["bot"],
    responses={404: {"description": "Not found"}},
)


@router.get("/bot/me", response_model=BotSchemaDbOut)
async def get_bot():
    bot = await get_bot_db(local_config.DATABASE_NAME)
    return bot
