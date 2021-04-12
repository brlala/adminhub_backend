from datetime import date, timedelta, datetime
from enum import Enum, auto

from app.server.db.collections import message_collection, bot_user_collection
from app.server.utils.common import form_query
from app.server.utils.timezone import make_timezone_aware


class DashboardSummary(Enum):
    USER = auto()
    MESSAGE = auto()
    CONVERSATION = auto()


class DashboardMessage:
    async def get_count(self, *, start: date = None, end: date = None) -> int:
        db_key = [("handler", "bot"),
                  ("created_at", {"$gte": make_timezone_aware(start)} if start else ...),
                  ("created_at", {"$lte": make_timezone_aware(end)} if end else ...)]
        query = form_query(db_key)

        return await message_collection.count_documents(query)


class DashboardUser:
    async def get_count(self, *, start: date = None, end: date = None) -> int:
        db_key = [("is_active", True),
                  ("created_at", {"$gte": make_timezone_aware(start)} if start else ...),
                  ("created_at", {"$lte": make_timezone_aware(end)} if end else ...)]
        query = form_query(db_key)

        return await bot_user_collection.count_documents(query)


class DashboardConversation:
    async def get_count(self, *, start: date = None, end: date = None) -> int:
        db_key = [("handler", "bot"),
                  ("created_at", {"$gte": make_timezone_aware(start)} if start else ...),
                  ("created_at", {"$lte": make_timezone_aware(end)} if end else ...)]
        query = form_query(db_key)

        pipeline = [{"$match": query},
                    {"$group": {"_id": None,
                                "count": {"$addToSet": "$chatbot.convo_id"}}},
                    {"$project": {"count": {"$size": "$count"}}}]

        cursor = message_collection.aggregate(pipeline)
        async for count in cursor:
            return count['count']

        return len(list(await message_collection.distinct("chatbot.convo_id", query)))


class Dashboard:
    _choice = {
        DashboardSummary.USER: DashboardUser,
        DashboardSummary.MESSAGE: DashboardMessage,
        DashboardSummary.CONVERSATION: DashboardConversation
    }

    def __init__(self, item: DashboardSummary):
        self.dashboard_summary = self._choice[item]()

    async def get_total_count(self) -> int:
        return await self.dashboard_summary.get_count()

    async def get_monthly_trend(self) -> (float, str):
        end_of_last_month = date.today().replace(day=1)  # get first day of this month and put it at 0:00
        start_of_last_month = (end_of_last_month - timedelta(days=1)).replace(day=1)
        count_last_month = await self.dashboard_summary.get_count(start=start_of_last_month, end=end_of_last_month)
        count_last_month = count_last_month or 1  # when zero count

        now = datetime.now()
        count_now = await self.dashboard_summary.get_count(start=end_of_last_month, end=now)
        normalized_count = (count_now / date.today().day) * 30
        return (normalized_count / count_last_month) - 1, (count_now, count_last_month)

    async def get_weekly_trend(self) -> (float, str):
        today = date.today()
        monday_of_this_week = today - timedelta(days=today.weekday())
        monday_of_last_week = today - timedelta(days=7)
        count_last_week = await self.dashboard_summary.get_count(start=monday_of_last_week, end=monday_of_this_week)
        count_last_week = count_last_week or 1  # when zero count

        now = datetime.now()
        count_now = await self.dashboard_summary.get_count(start=monday_of_this_week, end=now)
        normalized_count = (count_now / date.today().isoweekday()) * 7
        return (normalized_count / count_last_week) - 1, (count_now, count_last_week)

    async def get_today_count(self) -> int:
        start = date.today()
        now = datetime.now()
        count_now = await self.dashboard_summary.get_count(start=start, end=now)
        return count_now
