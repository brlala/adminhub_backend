from typing import Optional

from fastapi import APIRouter, Query, Depends

from ..db_utils.conversations import get_conversations_and_count_db
from ..db_utils.questions import get_topics_db, add_question_db, remove_questions_db, \
    edit_question_db
from ..models.current_user import CurrentUserSchema
from ..models.question import QuestionIn, DeleteQuestion
from ..utils.security import get_current_active_user

router = APIRouter(
    tags=["conversations"],
    prefix="/conversations",
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_conversations(tags: Optional[list[str]] = Query(None),
                            search_query: Optional[str] = Query(None, alias="searchQuery"),
                            current_page: int = Query(1, alias="current"),
                            page_size: int = Query(20, alias="pageSize"),
                            ):
    conversations, total = await get_conversations_and_count_db(current_page=current_page, page_size=page_size,
                                                                tags=tags, search_query=search_query)

    result = {
        "data": conversations,
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
