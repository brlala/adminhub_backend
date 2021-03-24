from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query, Depends

router = APIRouter(
    tags=["dashboard"],
    prefix="/dashboard",
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_questions():
    return 'test'