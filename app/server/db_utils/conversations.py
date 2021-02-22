from re import escape

from bson import Regex

from app.server.db.collections import bot_user_collection
from app.server.utils.common import form_query
from app.server.utils.timezone import make_timezone_aware


async def get_conversations_and_count_db(*, current_page: int, page_size: int, tags: list[str] = None,
                                         search_query: str) -> (list[QuestionSchemaDb], int):
    db_key = [(f"text.{language}", Regex(f".*{escape(question_text)}.*", "i") if question_text else ...)]
    query = form_query(db_key)

    questions = await get_conversations_db(current_page=current_page, page_size=page_size, query=query)
    total = await get_conversations_count_db(query=query)
    return questions, total


async def get_conversations_db(*, current_page: int, page_size: int, query: dict) -> list[QuestionSchemaDb]:
    # always show the newest first
    query = {}
    sort = [("last_active.sent_at", -1)]

    cursor = bot_user_collection.find(query, sort=sort)

    cursor = collection.find(query, sort=sort)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    questions = []
    async for question in cursor:
        questions.append(QuestionSchemaDb(**question_helper(question)))
    return questions


async def get_conversations_count_db(*, query: dict) -> int:
    count = collection.count_documents(query)
    return await count
