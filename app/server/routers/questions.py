from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel

from ..db_utils.flows import get_flow_one
from ..db_utils.questions import get_questions_and_count_db, get_topics_db, add_question_db, remove_questions_db
from ..models.current_user import CurrentUserSchema
from ..models.question import GetQuestionsTable, NewQuestion, DeleteQuestion
from ..utils.security import get_current_active_user

router = APIRouter(
    tags=["questions"],
    prefix="/questions",
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


@router.get("/", response_model=GetQuestionsTable)
async def get_questions(topic: Optional[str] = Query(None),
                        question_text: Optional[str] = Query(None, alias="questionText"),
                        created_at: Optional[datetime] = Query(None, alias="createdAt"),
                        updated_at: Optional[list[datetime]] = Query(None, alias="updatedAt"),
                        sort_by: str = Query(None, alias="sortBy"),
                        current_page: int = Query(1, alias="current"),
                        page_size: int = Query(20, alias="pageSize"),
                        language: str = 'EN'):
    questions, total = await get_questions_and_count_db(current_page=current_page, page_size=page_size,
                                                             sorter=sort_by, topic=topic,
                                                             question_text=question_text, language=language,
                                                             created_at=created_at, updated_at=updated_at)

    for q in questions:
        for a in q.answers:
            flow = await get_flow_one(a.flow['flow_id'])
            q.answer_flow = flow

    result = {
        "data": questions,
        "success": True,
        "total": total
    }
    return result


@router.post("/")
async def add_questions(question: NewQuestion, current_user: CurrentUserSchema = Depends(get_current_active_user)):
    await add_question_db(question, current_user)
    return True


@router.delete("/")
async def remove_questions(question: DeleteQuestion, current_user: CurrentUserSchema = Depends(get_current_active_user)):
    status = await remove_questions_db(question.key, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.get("/topics", response_model=list[str])
async def get_topics():
    topics = await get_topics_db()
    return topics
