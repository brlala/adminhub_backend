from bson import ObjectId

from app.server.db.collections import portal_user_group_collection


async def get_user_permissions(_id: str):
    """
    # Retrieve the correct portal_permissions
    :return:
    """
    pipeline = [
        {"$match": {"_id": ObjectId(_id)}},
        {"$lookup": {"from": "access_control",
                     "localField": "access_control_ids",
                     "foreignField": "_id",
                     "as": "permissions"}},
        {"$project": {"name": 1, "permissions": 1}}
    ]
    resp = {}
    async for doc in portal_user_group_collection.aggregate(pipeline):
        resp['access'] = doc['name']
        resp['permissions'] = [permission['name'] for permission in doc['permissions']]
        return resp
