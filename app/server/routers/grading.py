from fastapi import APIRouter, Query

from ..db_utils.grading import get_grading_messages_and_count_db
from ..models.message import GetMessagesTable, GetGradingsTable

router = APIRouter(
    tags=["gradings"],
    prefix='/gradings',
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=GetGradingsTable, response_model_exclude_none=True)
async def get_gradings_message(topic: str = Query(None),
                               search_query: str = Query(None, alias="searchQuery"),
                               accuracy: list[float] = Query([0, 1]),
                               ungraded: bool = Query(False),
                               current_page: int = Query(1, alias="current"),
                               page_size: int = Query(20, alias="pageSize")):
    messages, total = await get_grading_messages_and_count_db(topic=topic, search_query=search_query,
                                                              accuracy=accuracy, ungraded=ungraded,
                                                              current_page=current_page, page_size=page_size)

    result = {
        "data": messages,
        "success": True,
        "total": total
    }
    return result
