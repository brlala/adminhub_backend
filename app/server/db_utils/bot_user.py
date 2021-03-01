from bson import ObjectId

from app.server.db.collections import bot_user_collection as collection
from app.server.db_utils.helper import bot_user_helper
from app.server.models.bot_user import BotUserSchemaDb


async def get_bot_user_tags_db() -> list:
    """
    # Retrieve the correct portal user
    :return:
    """
    query = {"is_active": True}
    tags = await collection.distinct('tags', query)
    if tags:
        return tags
    else:
        return []


async def get_bot_user_db(user_id: str) -> BotUserSchemaDb:
    """
    # Retrieve the correct portal user
    :return:
    """
    query = {"_id": ObjectId(user_id)}
    return BotUserSchemaDb(**bot_user_helper(await collection.find_one(query)))
