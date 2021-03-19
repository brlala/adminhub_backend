from datetime import date

from bson import ObjectId

from app.server.db.collections import message_collection as collection
from app.server.db_utils.bot_user import get_bot_user_db
from app.server.db_utils.flows import get_flow_one
from app.server.db_utils.helper import message_helper
from app.server.db_utils.questions import get_question_one
from app.server.models.current_user import CurrentUserSchema
from app.server.models.message import MessageGradingSchemaDb, SkipMessage
from app.server.utils.common import form_query
from app.server.utils.timezone import get_local_datetime_now, make_timezone_aware


async def get_grading_messages_and_count_db(topic: str, search_query: str, accuracy: list[float],
                                            current_page: int, page_size: int, question_status: str, since: list[date]):
    if since:
        question_start = make_timezone_aware(since[0])
        question_end = make_timezone_aware(since[1])

    if question_status == 'Unanswered':
        db_key = [
            ("$text", {"$search": f"\"{search_query}\""} if search_query else ...),
            ("handler", "bot"),
            ("type", "message"),
            ("chatbot.unanswered", True),
            ("adminportal.graded", None),
            ("created_at", {"$gte": question_start, "$lte": question_end} if since else ...)
        ]
    elif question_status == 'Answered':
        db_key = [
            ("$text", {"$search": f"\"{search_query}\""} if search_query else ...),
            ("nlp.nlp_response.matched_questions.0.question_topic", topic if topic else ...),
            ("handler", "bot"),
            ("type", "message"),
            ("nlp", {"$ne": None}),
            ("chatbot.qnid", {"$ne": None}),
            ("nlp.nlp_response.matched_questions.0.score",
             {"$gte": accuracy[0] / 100, "$lte": accuracy[1] / 100} if accuracy else ...),
            ("created_at", {"$gte": question_start, "$lte": question_end} if since else ...)
        ]
    else:
        db_key = [
            ("$text", {"$search": f"\"{search_query}\""} if search_query else ...),
            ("nlp.nlp_response.matched_questions.0.question_topic", topic if topic else ...),
            ("handler", "bot"),
            ("type", "message"),
            ("nlp", {"$ne": None}),
            ("nlp.nlp_response.matched_questions.0.score",
             {"$gte": accuracy[0] / 100, "$lte": accuracy[1] / 100} if accuracy else ...),
            ("created_at", {"$gte": question_start, "$lte": question_end} if since else ...)
        ]
    query = form_query(db_key)
    sort = [("_id", -1)]
    cursor = collection.find(query, sort=sort)
    total = await collection.count_documents(query)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    messages = []
    async for message in cursor:
        user = await get_bot_user_db(message['sender_id'])
        try:
            message['fullname'] = f"{user.first_name} {user.last_name}"
        except:
            message['fullname'] = 'User'

        # flow
        if qnid := message.get('chatbot', {}).get('qnid'):
            question = await get_question_one(qnid)
            if question:
                for a in question.answers:
                    flow = await get_flow_one(a.flow['flow_id'])
                    message['answer_question'] = question
                    message['answer_flow'] = flow
        elif qns := message.get('nlp', {}).get('nlp_response', {}).get('matched_questions',
                                                                       {}):  # get first matched question if it does not have qnid(
            if len(qns) > 0:
                question = await get_question_one(qns[0]['question_id'])
                if question:
                    for a in question.answers:
                        flow = await get_flow_one(a.flow['flow_id'])
                        message['answer_question'] = question
                        message['answer_flow'] = flow

        messages.append(MessageGradingSchemaDb(**message_helper(message)))
    return messages, total


async def skip_message_db(message: SkipMessage, current_user: CurrentUserSchema) -> str:
    query = {"_id": ObjectId(message.id)}

    set_query = {
        "updated_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "adminportal.graded": True,
        "adminportal.answer": None
    }
    result = await collection.update_one(query, {'$set': set_query})

    return f"Skipped {result.modified_count} question."
