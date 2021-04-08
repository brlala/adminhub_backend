from datetime import datetime

from fastapi import APIRouter, Query

from app.server.db_utils.dashboard.summary import Dashboard, DashboardSummary
from app.server.db_utils.dashboard.top_search import question_ranking, top_topics_of_week, get_word_cloud

Message = Dashboard(DashboardSummary.MESSAGE)
User = Dashboard(DashboardSummary.USER)
Conversation = Dashboard(DashboardSummary.CONVERSATION)

router = APIRouter(
    tags=["dashboard"],
    prefix="/dashboard",
    responses={404: {"description": "Not found"}},
)


@router.get("/top-part/messages")
async def get_user_message():
    weekly_trend_percentage, weekly_trend_target = await Message.get_weekly_trend()
    monthly_trend_percentage, monthly_trend_target = await Message.get_monthly_trend()
    res = {
        "data": {
            "totalUserMessage": await Message.get_total_count(),
            "monthlyTrend": monthly_trend_percentage,
            "monthlyTarget": monthly_trend_target,
            "weeklyTrend": weekly_trend_percentage,
            "weeklyTarget": weekly_trend_target,
            "dailyUserMessage": await Message.get_today_count()
        },
        "status": True
    }
    return res


@router.get("/top-part/users")
async def get_users():
    weekly_trend_percentage, weekly_trend_target = await User.get_weekly_trend()
    monthly_trend_percentage, monthly_trend_target = await User.get_monthly_trend()
    res = {
        "data": {
            "totalUser": await User.get_total_count(),
            "monthlyTrend": monthly_trend_percentage,
            "monthlyTarget": monthly_trend_target,
            "weeklyTrend": weekly_trend_percentage,
            "weeklyTarget": weekly_trend_target,
            "dailyUser": await User.get_today_count()
        },
        "status": True
    }
    return res


@router.get("/top-part/conversations")
async def get_conversations():
    weekly_trend_percentage, weekly_trend_target = await Conversation.get_weekly_trend()
    monthly_trend_percentage, monthly_trend_target = await Conversation.get_monthly_trend()
    res = {
        "data": {
            "totalConversation": await Conversation.get_total_count(),
            "monthlyTrend": monthly_trend_percentage,
            "monthlyTarget": monthly_trend_target,
            "weeklyTrend": weekly_trend_percentage,
            "weeklyTarget": weekly_trend_target,
            "dailyConversation": await Conversation.get_today_count()
        },
        "status": True
    }
    return res


#
# @router.get("/middle-part/top-questions")
# async def top_question(since: list[date] = Query(None)):
#     weekly_trend_percentage, weekly_trend_target = await Conversation.get_weekly_trend()
#     monthly_trend_percentage, monthly_trend_target = await Conversation.get_monthly_trend()
#     res = {
#         "data": [
#             {
#                 "question"
#                 "count"
#                 "range"
#             }
#         ],
#         "status": True
#     }
#     return res

@router.get("/bottom-part/top-questions")
async def top_question(sort_by: str = Query(None, alias="sortBy")):
    today = datetime.now()
    # today = datetime(2020, 4, 12)
    data, total_model, average_model = await question_ranking(today, sorter=sort_by)
    res = {
        "data": {"table": data, "total": total_model, "average": average_model},
        "status": True
    }
    return res

@router.get("/bottom-part/top-topics")
async def top_question():
    today = datetime.now()
    today = datetime(2020, 4, 1)
    data = await top_topics_of_week(today)
    res = {
        "data": data,
        "date": today,
        "status": True
    }
    return res

@router.get("/bottom-part/word-cloud")
async def word_cloud():
    today = datetime.now()
    today = datetime(2020, 4, 1)
    res = {
        "data": await get_word_cloud(today),
        "status": True
    }
    return res
