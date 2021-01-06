from bson import ObjectId, Regex

from app.server.db.client import db

portal_user_collection = db['portal_user']


# def student_helper(student) -> dict:
#     return {
#         "id": str(student["_id"]),
#         "fullname": student["fullname"],
#         "email": student["email"],
#         "course_of_study": student["course_of_study"],
#         "year": student["year"],
#         "GPA": student["gpa"],
#     }

async def get_portal_user(username: str):
    """
    # Retrieve the correct portal user
    :return:
    """
    query = {"username": Regex(f"^{username}$", "i"), "is_active": True}
    async for user in portal_user_collection.find(query):
        return user
