from fastapi import APIRouter

from app.server.db_utils.dashboard import DashboardMessage
from fastapi import APIRouter

from app.server.db_utils.dashboard import DashboardMessage

Message = DashboardMessage()

router = APIRouter(
    tags=["dashboard"],
    prefix="/dashboard",
    responses={404: {"description": "Not found"}},
)


@router.get("/user-message")
async def get_questions():
    weekly_trend_percentage, weekly_trend_target = await Message.get_weekly_trend()
    monthly_trend_percentage, monthly_trend_target = await Message.get_monthly_trend()
    res = {
        "data": {
            "totalUserMessage": await Message.get_total_user_message(),
            "monthlyTrend": monthly_trend_percentage,
            "monthlyTarget": monthly_trend_target,
            "weeklyTrend": weekly_trend_percentage,
            "weeklyTarget": weekly_trend_target,
            "dailyUserMessage": await Message.get_today_user_message()
        },
        "status": True
    }
    return res
