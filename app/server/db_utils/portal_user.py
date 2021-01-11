from bson import ObjectId, Regex

from app.server.db.collections import portal_user_collection
from app.server.models.portal_user import PortalUserSchema


# def student_helper(student) -> dict:
#     return {
#         "id": str(student["_id"]),
#         "fullname": student["fullname"],
#         "email": student["email"],
#         "course_of_study": student["course_of_study"],
#         "year": student["year"],
#         "GPA": student["gpa"],
#     }

async def get_portal_user(username: str) -> PortalUserSchema:
    """
    # Retrieve the correct portal user
    :return:
    """
    query = {"username": Regex(f"^{username}$", "i"), "is_active": True}
    async for user in portal_user_collection.find(query):
        return PortalUserSchema(**user)
