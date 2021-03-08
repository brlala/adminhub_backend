from bson import ObjectId

from app.server.db.collections import bot_user_collection as collection
from app.server.db_utils.helper import bot_user_helper
from app.server.models.bot_user import BotUserSchemaDb, BotUserBasicSchemaDb


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


def bot_user_basic_information_helper(user: dict) -> dict:
    name_list = []
    if first_name := user["first_name"]:
        name_list.append(first_name)
    if last_name := user["last_name"]:
        name_list.append(last_name)
    if not name_list:
        name_list.append(str(user["_id"]))
    results = {
        "name": ' '.join(name_list),
        "id": str(user["_id"]),
    }
    return results


async def get_bot_users_by_tags_db(tags: list[str], exclude: list[str], toAll: bool) -> list[BotUserBasicSchemaDb]:
    """
    # Retrieve the correct portal user
    :return:
    """
    if toAll:
        query = {"tags": {"$nin": exclude}}
    else:
        query = {"tags": {"$in": tags, "$nin": exclude}}
    return [BotUserBasicSchemaDb(**bot_user_basic_information_helper(user)) async for user in collection.find(query)]


async def get_bot_user_db(user_id: str) -> BotUserSchemaDb:
    """
    # Retrieve the correct portal user
    :return:
    """
    query = {"_id": ObjectId(user_id)}
    return BotUserSchemaDb(**bot_user_helper(await collection.find_one(query)))


async def update_bot_user_db(user_id: str, *, tags: list[str]):
    new_values = {"$set": {"tags": tags}}
    result = await collection.update_one({"_id": ObjectId(user_id)}, new_values)
    return f"Updated {result.modified_count} bot user."
