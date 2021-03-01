from typing import Optional

from fastapi import APIRouter, Query

from ..db_utils.bot_user import get_bot_user_db
from ..db_utils.conversations import get_conversations_and_count_db, get_message_conversations_and_count_db, \
    get_user_message_conversations_and_count_db, get_convo_conversations_and_count_db
from ..models.bot_user import BotUserSchemaDb
from ..models.conversations import GetConversationsTable, GetConversationsMessageTable
from ..models.message import GetMessagesTable

router = APIRouter(
    tags=["Bot User"],
    prefix="/botuser",
    responses={404: {"description": "Not found"}},
)


@router.get("/{bot_user_id}", response_model_exclude_none=True, response_model=BotUserSchemaDb)
async def get_bot_user(bot_user_id: str):
    return await get_bot_user_db(bot_user_id)


@router.get("/messages", response_model_exclude_none=True, response_model=GetConversationsMessageTable)
async def get_conversations_message(search_query: Optional[str] = Query(None, alias="searchQuery"),
                                    current_page: int = Query(1, alias="current"),
                                    page_size: int = Query(20, alias="pageSize"),
                                    ):
    conversations, total = await get_message_conversations_and_count_db(current_page=current_page, page_size=page_size,
                                                                        search_query=search_query)

    result = {
        "data": conversations,
        "success": True,
        "total": total
    }
    return result


@router.get("/users/{user_id}", response_model_exclude_none=True, response_model=GetMessagesTable)
async def get_conversations_message(user_id: str = Query(None),
                                    current_page: int = Query(1, alias="current"),
                                    page_size: int = Query(20, alias="pageSize"),
                                    ):
    messages, total = await get_user_message_conversations_and_count_db(current_page=current_page, page_size=page_size,
                                                                        user_id=user_id)

    result = {
        "data": messages,
        "success": True,
        "total": total
    }
    return result


@router.get("/convos/{convo_id}", response_model_exclude_none=True, response_model=GetMessagesTable)
async def get_conversations_message(convo_id: str = Query(None),
                                    current_page: int = Query(1, alias="current"),
                                    page_size: int = Query(20, alias="pageSize"),
                                    ):
    messages, total = await get_convo_conversations_and_count_db(current_page=current_page, page_size=page_size,
                                                                 convo_id=convo_id)

    result = {
        "data": messages,
        "success": True,
        "total": total
    }
    return result
