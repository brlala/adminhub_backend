# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorDatabase
#
# from ..db.client import get_database
# from ...dependencies import get_token_header
#
# router = APIRouter(
#     prefix="/tests",
#     tags=["tests"],
#     responses={404: {"description": "Not found"}},
# )
#
# @router.get("/")
# async def read_items(db: AsyncIOMotorDatabase = Depends(get_database)):
#
#     async for student in db['portal_user'].find():
#         print(student)
#         # students.append(student)
#     # return students
#     return {"item_id": 'test', "name": "The great Plumbus"}