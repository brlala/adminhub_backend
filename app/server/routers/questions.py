from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from ..db_utils.questions import get_questions_from_db
from ..models.question import QuestionSchemaOut

router = APIRouter(
    tags=["questions"],
    responses={404: {"description": "Not found"}},
)


class CurrentUserParams(BaseModel):
    token: str

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZ…0OTJ9.rJ1WAF80i1EltnxAlfQI1PLJ9xrHH6qsw5Eeju9qB_w"
            }
        }


@router.get("/questions", response_model=list[QuestionSchemaOut])
async def get_questions(topic: Optional[str] = Query(None),
                        question_text: Optional[str] = Query(None, alias="questionText"),
                        created_at: Optional[datetime] = Query(None, alias="createdAt"),
                        sort_by: str = Query(None, alias="sortBy"),
                        current_page: int = Query(1, alias="currentPage"),
                        page_size: int = Query(20, alias="pageSize"),
                        language: str = 'EN'):
    questions = await get_questions_from_db(current_page=current_page, page_size=page_size, sorter=sort_by, topic=topic,
                                            question_text=question_text, language=language, created_at=created_at)
    return questions
