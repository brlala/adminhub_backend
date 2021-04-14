from datetime import datetime, date

from fastapi import APIRouter, Query

from app.server.db_utils.dashboard.summary import Dashboard, DashboardSummary, DashboardAnswerRate
from app.server.db_utils.dashboard.top_search import question_ranking, top_topics_of_week, get_word_cloud, \
    user_count_trend, message_count_trend, conversation_count_trend, nlp_confidence_trend, top_question

Message = Dashboard(DashboardSummary.MESSAGE)
User = Dashboard(DashboardSummary.USER)
Conversation = Dashboard(DashboardSummary.CONVERSATION)
AnswerRate = DashboardAnswerRate()

router = APIRouter(
    tags=["dashboard"],
    prefix="/dashboard",
    responses={404: {"description": "Not found"}},
)


@router.get("/top-part/messages")
async def get_user_message():
    weekly_trend_percentage, (wtd_count, count_last_week) = await Message.get_weekly_trend()
    monthly_trend_percentage, (mtd_count, count_last_month) = await Message.get_monthly_trend()
    res = {
        "data": {
            "total": await Message.get_total_count(),
            "monthlyTrend": monthly_trend_percentage,
            "monthlyTarget": {"count": mtd_count, "target": count_last_month},
            "weeklyTrend": weekly_trend_percentage,
            "weeklyTarget": {"count": wtd_count, "target": count_last_week},
            "daily": await Message.get_today_count()
        },
        "status": True
    }
    return res


@router.get("/top-part/users")
async def get_users():
    weekly_trend_percentage, (wtd_count, count_last_week) = await User.get_weekly_trend()
    monthly_trend_percentage, (mtd_count, count_last_month) = await User.get_monthly_trend()
    res = {
        "data": {
            "total": await User.get_total_count(),
            "monthlyTrend": monthly_trend_percentage,
            "monthlyTarget": {"count": mtd_count, "target": count_last_month},
            "weeklyTrend": weekly_trend_percentage,
            "weeklyTarget": {"count": wtd_count, "target": count_last_week},
            "daily": await User.get_today_count()
        },
        "status": True
    }
    return res


@router.get("/top-part/conversations")
async def get_conversations():
    weekly_trend_percentage, (wtd_count, count_last_week) = await Conversation.get_weekly_trend()
    monthly_trend_percentage, (mtd_count, count_last_month) = await Conversation.get_monthly_trend()
    res = {
        "data": {
            "total": await Conversation.get_total_count(),
            "monthlyTrend": monthly_trend_percentage,
            "monthlyTarget": {"count": mtd_count, "target": count_last_month},
            "weeklyTrend": weekly_trend_percentage,
            "weeklyTarget": {"count": wtd_count, "target": count_last_week},
            "daily": await Conversation.get_today_count()
        },
        "status": True
    }
    return res


@router.get("/top-part/answer-rate")
async def get_conversations():
    weekly_answered_count, weekly_unanswered_count, weekly_total = await AnswerRate.get_weekly_answered_count()
    monthly_answered_count, monthly_unanswered_count, monthly_total = await AnswerRate.get_monthly_answered_count()
    total_answered_count, total_unanswered_count, total = await AnswerRate.get_total_answered_count()
    res = {
        "data": {
            "total": {"answered": total_answered_count,
                      "unanswered": total_unanswered_count,
                      "total": total,
                      "rate": await AnswerRate.get_total_answered_rate()},
            "monthly": {"answered": monthly_answered_count,
                        "unanswered": monthly_unanswered_count,
                        "total": monthly_total,
                        "rate": await AnswerRate.get_monthly_answered_rate()},
            "weekly": {"answered": weekly_answered_count,
                       "unanswered": weekly_unanswered_count,
                       "total": weekly_total,
                       "rate": await AnswerRate.get_weekly_answered_rate()},
        },
        "status": True
    }
    return res


@router.post("/middle-part/user-trend")
async def user_trend(since: list[date]):
    res = {
        "data": await user_count_trend(since),
        "status": True
    }
    return res


@router.post("/middle-part/message-trend")
async def message_trend(since: list[date]):
    res = {
        "data": await message_count_trend(since),
        "status": True
    }
    return res


@router.post("/middle-part/conversation-trend")
async def message_trend(since: list[date]):
    res = {
        "data": await conversation_count_trend(since),
        "status": True
    }
    return res


@router.post("/middle-part/nlp-trend")
async def message_trend(since: list[date]):
    res = {
        "data": await nlp_confidence_trend(since),
        "status": True
    }
    return res


@router.post("/middle-part/top-question")
async def message_trend(since: list[date]):
    res = {
        "data": await top_question(since),
        "status": True
    }
    return res


@router.get("/bottom-part/questions-trend")
async def trend_question(sort_by: str = Query(None, alias="sortBy")):
    # today = datetime.now()
    today = datetime(2020, 4, 12)
    data, total_model, average_model = await question_ranking(today, sorter=sort_by)
    res = {
        "data": {"table": data, "total": total_model, "average": average_model},
        "status": True
    }
    return res


@router.get("/bottom-part/top-topics")
async def top_topics():
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
        "date": today,
        "status": True
    }
    return res
