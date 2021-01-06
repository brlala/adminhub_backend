from bson import ObjectId

from app.server.db.client import db

collection = db['portal_user_group']


# def student_helper(student) -> dict:
#     return {
#         "id": str(student["_id"]),
#         "fullname": student["fullname"],
#         "email": student["email"],
#         "course_of_study": student["course_of_study"],
#         "year": student["year"],
#         "GPA": student["gpa"],
#     }

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
    async for doc in collection.aggregate(pipeline):
        resp['access'] = doc['name']
        resp['permissions'] = [permission['name'] for permission in doc['permissions']]
        return resp
