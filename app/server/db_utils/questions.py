import uuid
from datetime import datetime
from re import escape

import stringcase
from bson import Regex, ObjectId

from app.server.db.collections import flow_collection
from app.server.db.collections import question_collection as collection
from app.server.db_utils.flows import add_flows_to_db
from app.server.models.current_user import CurrentUserSchema
from app.server.models.flow import NewFlow
from app.server.models.question import QuestionSchemaDb, QuestionIn
from app.server.utils.common import clean_dict_helper, form_query, Method
from app.server.utils.timezone import make_timezone_aware, get_local_datetime_now


def question_helper(question) -> dict:
    return {
        **question,
        "id": str(question["_id"]),
        "created_by": str(question["created_by"]),
        "updated_by": str(question["updated_by"]),
        "answers": clean_dict_helper(question["answers"])
    }


async def get_questions_db(*, current_page: int, page_size: int, sorter: str = None, query: dict) -> list[
    QuestionSchemaDb]:
    # always show the newest first
    sort = [("_id", -1)]
    if sorter:
        # [("answers", 1), ("bot_user_group", 1)]
        for s in sorter.split(','):
            order = s[:1]
            key = s[1:]
            if order == '+':
                sort.append((stringcase.snakecase(key), 1))
            else:
                sort.append((stringcase.snakecase(key), -1))

    cursor = collection.find(query, sort=sort)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    questions = []
    async for question in cursor:
        questions.append(QuestionSchemaDb(**question_helper(question)))
    return questions


async def get_questions_count_db(*, query: dict) -> int:
    count = collection.count_documents(query)
    return await count


async def get_questions_and_count_db(*, current_page: int, page_size: int, sorter: str = None, question_text: str,
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

    questions = await get_questions_db(current_page=current_page, page_size=page_size, sorter=sorter, query=query)
    total = await get_questions_count_db(query=query)
    return questions, total


async def get_topics_db():
    query = {"is_active": True}
    topics = await collection.distinct('topic', query)
    return topics


async def add_question_db(question: QuestionIn, current_user: CurrentUserSchema) -> str:
    doc = await process_question(question, current_user, method=Method.ADD)
    result = await collection.insert_one(doc)
    return f"Added {1 if result.acknowledged else 0} question."


async def process_question(question: QuestionIn, current_user: CurrentUserSchema, *, method: Method):
    variations = []
    if question.variations:
        for alt in question.variations.split('\n'):
            if not alt:
                continue
            variation = {
                "id": str(uuid.uuid4()),
                "text": alt.strip(),
                "language": question.language,
                "internal": False
            }
            variations.append(variation)

    question_start = question_end = None
    if question.question_time:
        question_start = make_timezone_aware(datetime.strptime(question.question_time[0], '%Y-%m-%d'))
        question_end = make_timezone_aware(datetime.strptime(question.question_time[1], '%Y-%m-%d'))

    if question.response_type == 'text':
        # if add, always create unnamed flow. if edit, find if there's exact flow(match topic and text)
        query = {f'flow.data.text.{question.language}': question.text_response, 'is_active': True,
                 "name": {"$exists": False}, "topic": question.topic}
        exist_response = await flow_collection.find_one(query)
        if exist_response:
            flow_id = exist_response['_id']
        else:  # create unnamed response
            flow_doc = [{"type": "message", "data": {"text": {question.language: question.text_response}}}]
            flow = NewFlow(**{"topic": question.topic, "type": "storyboard", "flow_items": flow_doc})
            flow_id = await add_flows_to_db(flow, current_user)
    else:  # question.response_type == 'flow'
        flow_id = question.flow_response
    doc = {
        "created_at": get_local_datetime_now(),
        "created_by": ObjectId(current_user.userId),
        "updated_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "text": {question.language: question.main_question},
        "internal": False,
        "keyword": question.tags,
        "answers": [
            {
                "id": "1",
                "flow": {"flow_id": ObjectId(flow_id)},
                "bot_user_group": "1"
            }
        ],
        "alternate_questions": variations,
        "topic": question.topic,
        "active_at": question_start,
        "expire_at": question_end,
        "is_active": True
    }

    if method == Method.EDIT:
        keys_to_remove = ["created_at", "created_by"]
        for key in keys_to_remove:
            doc.pop(key)
    return doc


async def edit_question_db(question: QuestionIn, current_user: CurrentUserSchema):
    doc = await process_question(question, current_user, method=Method.EDIT)
    new_values = {"$set": doc}
    result = await collection.update_one({"_id": ObjectId(question.id)}, new_values)
    return f"Updated {result.modified_count} question."


async def remove_questions_db(question_ids: list[str], current_user: CurrentUserSchema) -> str:
    query = {"_id": {"$in": [ObjectId(q) for q in question_ids]}, "is_active": True}
    linked_flows = await collection.distinct('answers.flow.flow_id', query)

    # delete questions
    set_query = {
        "updated_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "is_active": False
    }
    result1 = await collection.update_many(query, {'$set': set_query})

    # delete flows related
    query = {"_id": {"$in": linked_flows}, "name": {"$exists": False}, "is_active": True}
    result2 = await flow_collection.update_many(query, {'$set': set_query})
    return f"Removed {result1.modified_count} questions and {result2.modified_count} linked flows."
