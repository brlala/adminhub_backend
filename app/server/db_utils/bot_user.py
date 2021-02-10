from bson import ObjectId, Regex

from app.server.db.collections import bot_user_collection as collection


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
