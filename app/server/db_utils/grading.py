from re import escape

import stringcase
from bson import Regex

from app.server.db.collections import message_collection as collection
from app.server.db_utils.bot_user import get_bot_user_db
from app.server.db_utils.flows import get_flow_one
from app.server.db_utils.helper import message_helper
from app.server.db_utils.questions import get_question_one
from app.server.models.message import MessageSchemaDb, MessageGradingSchemaDb
from app.server.utils.common import form_query


async def get_grading_messages_and_count_db(topic: str, search_query: str, accuracy: list[float], ungraded: bool,
                                            current_page: int, page_size: int):
    if ungraded:
        db_key = [
            (f"data.text", Regex(f".*{escape(search_query)}.*", "i") if search_query else ...),
            (f"chatbot.unanswered", True),
            ("adminportal", {"$exists": False})]
    else:
        db_key = [
            ("nlp.nlp_response.matched_questions.0.question_text",
             Regex(f".*{escape(search_query)}.*", "i") if search_query else ...),
            ("nlp.nlp_response.matched_questions.0.question_topic", topic if topic else ...),
            ("nlp.nlp_response.matched_questions.0.score", {"$gte": accuracy[0], "$lte": accuracy[1]})]
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
            for a in question.answers:
                flow = await get_flow_one(a.flow['flow_id'])
                message['answer_question'] = question
                message['answer_flow'] = flow
        messages.append(MessageGradingSchemaDb(**message_helper(message)))
    return messages, total
