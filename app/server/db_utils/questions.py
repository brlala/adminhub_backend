import asyncio
from datetime import datetime
from re import escape

import stringcase
from bson import Regex

from app.server.db.client import db
from app.server.models.question import QuestionSchemaDb
from app.server.utils.common import clean_dict_helper, form_query

question_user_collection = db['question']


def question_helper(question) -> dict:
    return {
        **question,
        "id": str(question["_id"]),
        "created_by": str(question["created_by"]),
        "updated_by": str(question["updated_by"]),
        "answers": clean_dict_helper(question["answers"])
    }


async def get_questions_from_db(*, current_page: int, page_size: int, sorter: str = None, question_text: str,
                                language: str, topic: str, created_at: datetime) -> list[QuestionSchemaDb]:
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

    db_key = [("topic", topic if topic else ...),
              (f"text.{language}", Regex(f".*{escape(question_text)}.*", "i") if question_text else ...),
              ("created_at", created_at if created_at else ...),
              ("is_active", True)]

    query = form_query(db_key)

    cursor = question_user_collection.find(query, sort=sort)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    questions = []
    async for question in cursor:
        questions.append(QuestionSchemaDb(**question_helper(question)))
    return questions


async def get_questions_count_from_db(*, question_text: str, language: str, topic: str, created_at: datetime) -> int:
    db_key = [("topic", topic if topic else ...),
              (f"text.{language}", Regex(f".*{escape(question_text)}.*", "i") if question_text else ...),
              ("created_at", created_at if created_at else ...),
              ("is_active", True)]

    query = form_query(db_key)
    print(query)
    count = question_user_collection.count_documents(query)
    return await count


async def get_questions_and_count_from_db(*, current_page: int, page_size: int, sorter: str = None, question_text: str,
                                          language: str, topic: str, created_at: datetime) -> (list[QuestionSchemaDb], int):
    questions = await get_questions_from_db(current_page=current_page, page_size=page_size, sorter=sorter, topic=topic,
                              question_text=question_text, language=language, created_at=created_at)
    total = await get_questions_count_from_db(question_text=question_text, language=language, created_at=created_at, topic=topic)
    return questions, total


