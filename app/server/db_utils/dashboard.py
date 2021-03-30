from datetime import date, timedelta, datetime

from app.server.db.collections import message_collection as collection
from app.server.utils.common import form_query
from app.server.utils.timezone import make_timezone_aware


class DashboardMessage:
    async def get_total_user_message(self) -> int:
        return await self.get_count_user_message()

    async def get_monthly_trend(self) -> (float, str):
        end_of_last_month = date.today().replace(day=1)  # get first day of this month and put it at 0:00
        start_of_last_month = (end_of_last_month - timedelta(days=1)).replace(day=1)
        count_last_month = await self.get_count_user_message(start=start_of_last_month, end=end_of_last_month)

        now = datetime.now()
        count_now = await self.get_count_user_message(start=end_of_last_month, end=now)
        return count_now / count_last_month, f"{count_now}/{count_last_month}"

    async def get_weekly_trend(self) -> (float, str):
        today = date.today()
        monday_of_this_week = today - timedelta(days=today.weekday())
        monday_of_last_week = today - timedelta(days=7)
        count_last_week = await self.get_count_user_message(start=monday_of_last_week, end=monday_of_this_week)

        now = datetime.now()
        count_now = await self.get_count_user_message(start=monday_of_this_week, end=now)
        return count_now / count_last_week, f"{count_now}/{count_last_week}"

    async def get_today_user_message(self) -> int:
        start = date.today()
        now = datetime.now()
        count_now = await self.get_count_user_message(start=start, end=now)
        return count_now

    async def get_count_user_message(self, *, start: date = None, end: date = None) -> int:
        db_key = [("handler", "bot"),
                  ("created_at", {"$gte": make_timezone_aware(start)} if start else ...),
                  ("created_at", {"$lte": make_timezone_aware(end)} if end else ...)]
        query = form_query(db_key)

        return await collection.count_documents(query)


class DashboardUser:
    async def get_total_user_message(self) -> int:
        return await self.get_count_user_message()

    async def get_monthly_trend(self) -> float:
        end_of_last_month = date.today().replace(day=1)  # get first day of this month and put it at 0:00
        count_last_month = await self.get_count_user_message(end=end_of_last_month)

        now = datetime.now()
        count_now = await self.get_count_user_message(start=end_of_last_month, end=now)
        return count_now / count_last_month

    async def get_weekly_trend(self) -> float:
        today = date.today()
        monday_of_week = today - timedelta(days=today.weekday())
        count_last_week = await self.get_count_user_message(end=monday_of_week)

        now = datetime.now()
        count_now = await self.get_count_user_message(start=monday_of_week, end=now)
        return count_now / count_last_week

    async def get_today_user_message(self) -> int:
        start = date.today()
        now = datetime.now()
        count_now = await self.get_count_user_message(start=start, end=now)
        return count_now

    async def get_count_user_message(self, *, start: date = None, end: date = None) -> int:
        db_key = [("handler", "bot"),
                  ("created_at", {"$gte": make_timezone_aware(start)} if start else ...),
                  ("created_at", {"$lte": make_timezone_aware(end)} if end else ...)]
        query = form_query(db_key)

        return await collection.count_documents(query)
