from bson import SON, ObjectId

from app.server.db.collections import bot_user_collection
from app.server.db.collections import message_collection
from app.server.models.conversations import ConversationBotUserSchema, ConversationMessageUserSchema
from app.server.models.flow import FlowTypeEnumOut
from app.server.models.message import MessageSchemaDb
from app.server.utils.common import clean_dict_helper, form_pipeline


def bot_user_helper(bot_user) -> dict:
    return {
        **bot_user,
        "id": str(bot_user["_id"]),
        "last_active": clean_dict_helper(bot_user["last_active"]) if bot_user.get("last_active") else None,
        "last_message": clean_dict_helper(message_helper(bot_user['last_message'])) if bot_user.get(
            'last_message') else None
    }


def message_helper(message) -> dict:
    message['type'] = str(FlowTypeEnumOut(message['type']))
    return clean_dict_helper({
        **message,
        "id": str(message["_id"]),
    })


def convo_message_search_helper(message) -> dict:
    return {
        **message,
        "user": clean_dict_helper(bot_user_helper(message["user"])) if message.get("user") else None,
        "id": str(message["_id"]),
    }


async def get_conversations_and_count_db(*, current_page: int, page_size: int, tags: list[str] = None,
                                         search_query: str = ''):
    conversations = []
    db_key = [("$addFields", {"fullname": {"$concat": ["$last_name", " ", "$first_name"]}}),
              ("$match", {"tags": tags} if tags else ...)]
    pipeline = form_pipeline(db_key)
    total = await bot_user_pipeline_count(pipeline=pipeline[:])
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


async def get_message_conversations_and_count_db(*, current_page: int, page_size: int, search_query: str):
    conversations = []
    pipeline = [{"$match": {"$text": {"$search": f"\"{search_query}\"" if search_query else ''}}},
                {"$sort": SON([("_id", -1)])},
                {"$group": {"_id": "$sender_id",
                            "convo_id": {
                                "$addToSet": "$chatbot.convo_id"
                            },
                            "last_message_date": {
                                "$first": "$created_at"}}}]
    total = await message_pipeline_count(pipeline=pipeline[:])
    extra_stages = [{"$sort": SON([("last_message_date", -1)])},
                    {"$skip": (current_page - 1) * page_size},
                    {"$limit": page_size},
                    {"$lookup": {
                        "from": "bot_user",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "user"}},
                    {"$unwind": {"path": "$user"}},
                    # {"$match": {"user.tags": tags}},
                    {"$addFields": {"fullname": {"$concat": ["$user.last_name", " ", "$user.first_name"]},
                                    "convo_count": {"$size": "$convo_id"}}}]
    pipeline.extend(extra_stages)

    cursor = message_collection.aggregate(pipeline)

    async for conversation in cursor:
        conversations.append(ConversationMessageUserSchema(**convo_message_search_helper(conversation)))
    return conversations, total


async def get_user_message_conversations_and_count_db(*, current_page: int, page_size: int, user_id: str):
    messages = []
    query = {"$or": [{"sender_id": ObjectId(user_id)},
                     {"receiver_id": ObjectId(user_id)}]}
    sort = [("_id", -1)]
    total = await message_query_count(query=query)
    cursor = message_collection.find(query, sort=sort)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    async for conversation in cursor:
        messages.append(MessageSchemaDb(**message_helper(conversation)))
    return messages, total


async def get_convo_conversations_and_count_db(*, current_page: int, page_size: int, convo_id: str):
    messages = []
    query = {"chatbot.convo_id": convo_id}
    sort = [("_id", -1)]
    total = await message_query_count(query=query)
    cursor = message_collection.find(query, sort=sort)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    async for conversation in cursor:
        messages.append(MessageSchemaDb(**message_helper(conversation)))
    return messages, total


async def bot_user_pipeline_count(*, pipeline: list[dict]) -> int:
    pipeline.append({"$count": "total_count"})
    cursor = bot_user_collection.aggregate(pipeline)
    total = 0
    async for conversations in cursor:
        total = conversations['total_count']
    return total


async def message_pipeline_count(*, pipeline: list[dict]) -> int:
    pipeline.append({"$count": "total_count"})
    cursor = message_collection.aggregate(pipeline)
    total = 0
    async for conversations in cursor:
        total = conversations['total_count']
    return total


async def message_query_count(*, query: dict) -> int:
    count = message_collection.count_documents(query)
    return await count
