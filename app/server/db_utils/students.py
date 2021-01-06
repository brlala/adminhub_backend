from bson import ObjectId

from app.server.db.client import db

portal_user_collection = db['students_collection']


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


async def retrieve_students():
    """
    # Retrieve all students present in the database
    :return:
    """
    students = []
    async for student in portal_user_collection.find():
        students.append(student_helper(student))
    return students


async def add_student(student_data: dict) -> dict:
    """
    # Add a new student into to the database
    :param student_data:
    :return:
    """
    student = await portal_user_collection.insert_one(student_data)
    new_student = await portal_user_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


async def retrieve_student(id: str) -> dict:
    """
    # Retrieve a student with a matching ID
    :param id:
    :return:
    """
    student = await portal_user_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


async def update_student(id: str, data: dict):
    """
    # Update a student with a matching ID
    :param id:
    :param data:
    :return:
    """
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await portal_user_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await portal_user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


async def delete_student(id: str):
    """
    # Delete a student from the database
    :param id:
    :return:
    """
    student = await portal_user_collection.find_one({"_id": ObjectId(id)})
    if student:
        await portal_user_collection.delete_one({"_id": ObjectId(id)})
        return True
