from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel

from ..db_utils.flows import get_flow_one
from ..db_utils.questions import get_questions_and_count_db, get_topics_db, add_question_db, remove_questions_db, \
    edit_question_db, get_question_filtered_field_list
from ..models.current_user import CurrentUserSchema
from ..models.question import GetQuestionsTable, QuestionIn, DeleteQuestion
from ..utils.common import Status
from ..utils.security import get_current_active_user
from ..utils.timezone import get_local_datetime_now

router = APIRouter(
    tags=["questions"],
    prefix="/questions",
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=GetQuestionsTable, response_model_exclude_none=True)
async def get_questions(topic: Optional[str] = Query(None),
                        question_text: Optional[str] = Query(None, alias="questionText"),
                        created_at: Optional[datetime] = Query(None, alias="createdAt"),
                        updated_at: Optional[list[date]] = Query(None, alias="updatedAt"),
                        sort_by: str = Query(None, alias="sortBy"),
                        current_page: int = Query(1, alias="current"),
                        page_size: int = Query(20, alias="pageSize"),
                        triggered_counts: list[int] = Query(None, alias="triggeredCount"),
                        language: str = 'EN'):
    questions, total = await get_questions_and_count_db(current_page=current_page, page_size=page_size,
                                                        sorter=sort_by, topic=topic,
                                                        question_text=question_text, language=language,
                                                        updated_at=updated_at,
                                                        triggered_counts=triggered_counts)

    for q in questions:
        q.status = Status.ACTIVE
        if q.active_at:
            if q.active_at <= get_local_datetime_now() <= q.expire_at:
                q.status = Status.SCHEDULE
            else:
                q.status = Status.INACTIVE

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
async def add_question(question: QuestionIn, current_user: CurrentUserSchema = Depends(get_current_active_user)):
    status = await add_question_db(question, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.delete("/")
async def remove_questions(question: DeleteQuestion,
                           current_user: CurrentUserSchema = Depends(get_current_active_user)):
    status = await remove_questions_db(question.key, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.put("/")
async def edit_question(question: QuestionIn, current_user: CurrentUserSchema = Depends(get_current_active_user)):
    status = await edit_question_db(question, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.get("/topics", response_model=list[str])
async def get_topics():
    topics = await get_topics_db()
    return topics


@router.get("/fields")
async def get_questions_filtered(field: Optional[str] = None):
    flows = await get_question_filtered_field_list(field)
    return flows
