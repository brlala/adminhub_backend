from app.server.db.collections import bot_collection
from app.server.models.bot import BotSchemaDb
from app.server.utils.common import clean_dict_helper


def bot_helper(bot):
    results = {
        **bot,
        "id": str(bot["_id"]),
    }
    return clean_dict_helper(results)


async def get_bot_db(abbr: str) -> BotSchemaDb:
    query = {"abbreviation": abbr, "is_active": True}
    print(query)
    async for bot in bot_collection.find(query):
        return BotSchemaDb(**bot_helper(bot))
