from re import escape

from bson import SON, Regex

from app.server.db.collections import bot_user_collection
from app.server.models.conversations import ConversationBotUserSchema
from app.server.models.flow import FlowTypeEnumOut
from app.server.utils.common import clean_dict_helper, form_query, form_pipeline


def bot_user_helper(bot_user) -> dict:
    return {
        **bot_user,
        "id": str(bot_user["_id"]),
        "last_active": clean_dict_helper(bot_user["last_active"]) if bot_user["last_active"] else None,
        "last_message": clean_dict_helper(message_helper(bot_user['last_message'])) if bot_user[
            'last_message'] else None
    }


def message_helper(message) -> dict:
    message['type'] = str(FlowTypeEnumOut(message['type']))
    return {
        **message,
        "id": str(message["_id"]),
    }


async def get_conversations_and_count_db(*, current_page: int, page_size: int, tags: list[str] = None,
                                         search_query: str = ''):
    conversations = []
    db_key = [("$addFields", {"fullname": {"$concat": ["$last_name", " ", "$first_name"]}}),
              ("$match", {"tags": tags} if tags else ...),
              ("$match", {"fullname": Regex(f".*{escape(search_query)}.*", "i")} if search_query else ...)]
    pipeline = form_pipeline(db_key)
    total = await get_conversations_count_db(pipeline=pipeline[:])
    extra_stages = [
        {"$sort": SON([("last_active.sent_at", -1)])},
        {"$skip": (current_page - 1) * page_size},
        {"$limit": page_size},
        {"$lookup": {
            "from": "message",
            "localField": "last_active.sent_message_id",
            "foreignField": "_id",
            "as": "message"}},
        {"$unwind": {
            "path": "$message",
            "preserveNullAndEmptyArrays": False
        }},
        {"$lookup": {
            "from": "message",
            "localField": "message.chatbot.convo_id",
            "foreignField": "chatbot.convo_id",
            "as": "conversations"
        }},
        {"$addFields": {
            "last_message": {
                "$last": "$conversations"
            }
        }},
        {"$project": {
            "_id": 1,
            "fullname": 1,
            "first_name": 1,
            "last_name": 1,
            "email": 1,
            "gender": 1,
            "profile_pic_url": 1,
            "last_active": 1,
            "created_at": 1,
            "chatbot": 1,
            "tags": 1,
            "platforms": 1,
            "last_message": 1
        }}
    ]

    pipeline.extend(extra_stages)

    cursor = bot_user_collection.aggregate(pipeline)

    async for conversation in cursor:
        conversations.append(ConversationBotUserSchema(**bot_user_helper(conversation)))
    return conversations, total
    # db_key = [(f"text.{language}", Regex(f".*{escape(question_text)}.*", "i") if question_text else ...)]
    # query = form_query(db_key)
    #
    # questions = await get_conversations_db(current_page=current_page, page_size=page_size, query=query)
    # total = await get_conversations_count_db(query=query)
    # return questions, total


#
# async def get_conversations_db(*, current_page: int, page_size: int, query: dict):
#     # always show the newest first
#     query = {}
#     sort = [("last_active.sent_at", -1)]
#
#     cursor = bot_user_collection.find(query, sort=sort)
#
#     cursor = collection.find(query, sort=sort)
#     cursor.skip((current_page - 1) * page_size).limit(page_size)
#     questions = []
#     async for question in cursor:
#         questions.append(QuestionSchemaDb(**question_helper(question)))
#     return questions


async def get_conversations_count_db(*, pipeline: list[dict]) -> int:
    pipeline.append({"$count": "total_count"})
    cursor = bot_user_collection.aggregate(pipeline)
    async for conversations in cursor:
        total = conversations['total_count']
        return total if total else 0
