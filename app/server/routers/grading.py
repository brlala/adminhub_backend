from datetime import date

from fastapi import APIRouter, Query

from ..db_utils.grading import get_grading_messages_and_count_db, skip_message_db, update_message_db
from ..models.current_user import CurrentUserSchema
from ..models.message import GetGradingsTable, SkipMessage, UpdateMessageResponse

router = APIRouter(
    tags=["gradings"],
    prefix='/gradings',
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=GetGradingsTable, response_model_exclude_none=True)
async def get_gradings_message(topic: str = Query(None),
                               search_query: str = Query(None, alias="text"),
                               accuracy: list[float] = Query(None),
                               current_page: int = Query(1, alias="current"),
                               page_size: int = Query(20, alias="pageSize"),
                               question_status: str = Query(None, alias="questionStatus"),
                               since: list[date] = Query(None)):
    messages, total = await get_grading_messages_and_count_db(topic=topic, search_query=search_query,
                                                              accuracy=accuracy, question_status=question_status,
                                                              current_page=current_page, page_size=page_size,
                                                              since=since)

    result = {
        "data": messages,
        "success": True,
        "total": total
    }
    return result


@router.delete("/")
async def skip_questions(message: SkipMessage,
                         # current_user: CurrentUserSchema = Depends(get_current_active_user)
                         ):
    current_user = CurrentUserSchema(**{
        "username": "user@pand.ai",
        "userId": "5efdc63e74f7e093ce73db78",
        "access": "admin",
        "permissions": [
            "create_flow",
            "read_flow",
        ],
        "name": "Teh Li heng ",
        "email": "liheng@pand.ai",
        "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
        "is_active": True
    })
    status = await skip_message_db(message, current_user)
    return {
        "status": status,
        "success": True,
    }


@router.patch("/")
async def update_message_response(message: UpdateMessageResponse,
                                  # current_user: CurrentUserSchema = Depends(get_current_active_user)
                                  ):
    current_user = CurrentUserSchema(**{
        "username": "user@pand.ai",
        "userId": "5efdc63e74f7e093ce73db78",
        "access": "admin",
        "permissions": [
            "create_flow",
            "read_flow",
        ],
        "name": "Teh Li heng ",
        "email": "liheng@pand.ai",
        "avatar": "https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png",
        "is_active": True
    })
    status = await update_message_db(message, current_user)
    return {
        "status": status,
        "success": True,
    }
