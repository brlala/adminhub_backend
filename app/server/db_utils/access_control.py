from bson import Regex

from app.server.db.collections import portal_user_collection


async def get_portal_user(username: str):
    """
    # Retrieve the correct portal user
    :return:
    """
    query = {"username": Regex(f"^{username}$", "i"), "is_active": True}
    async for user in portal_user_collection.find(query):
        return user
