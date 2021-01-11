from datetime import datetime
from re import escape

import stringcase
from bson import Regex

from app.server.db.collections import question_user_collection
from app.server.models.question import QuestionSchemaDb
from app.server.utils.common import clean_dict_helper, form_query
from app.server.utils.timezone import make_timezone_aware


def question_helper(question) -> dict:
    return {
        **question,
        "id": str(question["_id"]),
        "created_by": str(question["created_by"]),
        "updated_by": str(question["updated_by"]),
        "answers": clean_dict_helper(question["answers"])
    }


async def get_questions_from_db(*, current_page: int, page_size: int, sorter: str = None, query: dict) -> list[
    QuestionSchemaDb]:
    sort = []
    if sorter:
        # [("answers", 1), ("bot_user_group", 1)]
        for s in sorter.split(','):
            order = s[:1]
            key = s[1:]
            if order == '+':
                sort.append((stringcase.snakecase(key), 1))
            else:
                sort.append((stringcase.snakecase(key), -1))

    cursor = question_user_collection.find(query, sort=sort)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    questions = []
    async for question in cursor:
        questions.append(QuestionSchemaDb(**question_helper(question)))
    return questions


async def get_questions_count_from_db(*, query: dict) -> int:
    count = question_user_collection.count_documents(query)
    return await count


async def get_questions_and_count_from_db(*, current_page: int, page_size: int, sorter: str = None, question_text: str,
                                          language: str, topic: str, created_at: datetime,
                                          updated_at: list[datetime]) -> (list[QuestionSchemaDb], int):
    if updated_at:
        updated_at_start, updated_at_end = updated_at
    if created_at:
        created_at_start, created_at_end = created_at
    db_key = [("topic", Regex(f".*{escape(topic)}.*", "i") if topic else ...),
              (f"text.{language}", Regex(f".*{escape(question_text)}.*", "i") if question_text else ...),
              ("created_at", {"$gte": make_timezone_aware(created_at_start),
                              "$lte": make_timezone_aware(created_at_end)} if created_at else ...),
              ("is_active", True),
              ("updated_at", {"$gte": make_timezone_aware(updated_at_start),
                              "$lte": make_timezone_aware(updated_at_end)} if updated_at else ...)]
    query = form_query(db_key)

    questions = await get_questions_from_db(current_page=current_page, page_size=page_size, sorter=sorter, query=query)
    total = await get_questions_count_from_db(query=query)
    return questions, total
