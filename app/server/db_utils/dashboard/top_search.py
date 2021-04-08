from datetime import timedelta, datetime, date

from bson import SON
from pydantic.main import BaseModel

from app.server.db.collections import message_collection
from app.server.db_utils.helper import common_helper
from app.server.models.dashboard import QuestionRankingDataModel
from app.server.routers.word_cloud.stop_words import default_stop_words
from app.server.utils.timezone import make_timezone_aware


class DecayModel(BaseModel):
    count: float
    text: str
    total: int


def decay(old: list[QuestionRankingDataModel], new: list[QuestionRankingDataModel]) -> dict:
    past_day7 = {q.id: {"count": q.count * 0.875, "text": q.text, "total": q.count} for q in new}
    past_day1_6 = {q.id: {"count": q.count * 0.125, "text": q.text, "total": q.count} for q in old}
    res = {}
    for key, value in past_day7.items():
        if key in past_day1_6:
            res[key] = DecayModel(**{"count": past_day7[key]['count'] + past_day1_6[key]['count'],
                                     "text": value['text'],
                                     "total": past_day7[key]['total'] + past_day1_6[key]['total']})
        else:
            entry = past_day7.get(key) or past_day1_6.get(key)
            res[key] = DecayModel(**{"count": entry['count'],
                                     "text": entry['text'],
                                     "total": entry['total']
                                     })
    return res


async def question_ranking(today: datetime, *, sorter: str = None):
    recent_day7 = await get_question_trend(start=today, end=today + timedelta(days=1), language='EN')
    recent_day1_6 = await get_question_trend(start=(today - timedelta(days=6)), end=today,
                                             language='EN')
    past_day7 = await get_question_trend(start=(today - timedelta(days=1)), end=today, language='EN')
    past_day1_6 = await get_question_trend(start=(today - timedelta(days=7)), end=today - timedelta(days=1),
                                           language='EN')

    recent = decay(recent_day1_6, recent_day7)
    past = decay(past_day1_6, past_day7)

    data = await question_ranking_data(recent, past, sorter=sorter)
    total_model = await question_ranking_total(recent, past, today)
    average_model = await question_ranking_average(recent, past, today)
    return data, total_model, average_model


async def question_ranking_data(recent, past, sorter):
    """
    -1 means question is not asked recently, -0.12% means decreasing interest of 12%, 0.04 means increasing interest of 4%
    """
    res = []
    for item in recent.items():
        key = item[0]
        value: DecayModel = item[1]

        temp = {
            "text": value.text,
            "count": value.total,
            "trend": 0
        }
        if key in past:
            temp['trend'] = (recent[key].count / past[key].count) - 1 if recent.get(key) else -1

        res.append(temp)

    if sorter:  # +count
        # trend +,-| count +,-
        order = sorter[:1]
        key = sorter[1:]
        if order == '+':
            res = sorted(res, key=lambda x: (-x[key]))
        else:
            res = sorted(res, key=lambda x: (x[key]))
    else:
        res = sorted(res, key=lambda x: (-x['trend'], -x['count']))
    for index, r in enumerate(res, 1):
        r['rank'] = index
    return res


class QuestionTotalHistoryViewModel(BaseModel):
    date: date
    count: int


class QuestionTotalViewModel(BaseModel):
    value: int
    trend: float
    history: list[QuestionTotalHistoryViewModel]


async def question_ranking_total(recent, past, today: date) -> (int, float, list[dict]):
    today = today.today()  # ignore time
    recent_total = sum([value.count for key, value in recent.items()])
    past_total = sum([value.count for key, value in past.items()])
    total_trend = recent_total / past_total if past_total else 0
    history = []
    # get past 7 days total
    start_date = today - timedelta(days=7)
    end_date = today
    one_day_delta = timedelta(days=1)
    while start_date <= end_date:
        query = {"chatbot.qnid": {"$exists": True},
                 "created_at": {"$gte": make_timezone_aware(start_date),
                                "$lte": make_timezone_aware(start_date + one_day_delta)}}

        count = await message_collection.count_documents(query)
        history.append(QuestionTotalHistoryViewModel(**{"date": start_date, "count": count}))
        start_date += one_day_delta
    return QuestionTotalViewModel(**{"value": recent_total, "trend": total_trend, "history": history})


class QuestionAverageHistoryViewModel(BaseModel):
    date: date
    average: float


class QuestionAverageViewModel(BaseModel):
    value: float
    trend: float
    history: list[QuestionAverageHistoryViewModel]


async def question_ranking_average(recent, past, today: date) -> (int, float, list[dict]):
    today = today.today()  # ignore time
    recent_average = sum([value.count for key, value in recent.items()]) / len(recent) if len(recent) else 0
    past_average = sum([value.count for key, value in past.items()]) / len(recent) if len(recent) else 0
    average_trend = recent_average / past_average if past_average else 0
    history = []
    # get past 7 days average
    start_date = today - timedelta(days=7)
    end_date = today
    one_day_delta = timedelta(days=1)
    while start_date <= end_date:
        query = {"chatbot.qnid": {"$exists": True},
                 "created_at": {"$gte": make_timezone_aware(start_date),
                                "$lte": make_timezone_aware(start_date + one_day_delta)}}

        count = await message_collection.count_documents(query)
        question = await message_collection.distinct('chatbot.qnid', query)
        average = count / len(question) if count else 0
        history.append(QuestionAverageHistoryViewModel(**{"date": start_date, "average": average}))
        start_date += one_day_delta
    return QuestionAverageViewModel(**{"value": recent_average, "history": history, "trend": average_trend})


async def get_question_trend(*, start: datetime = None, end: datetime = None, language):
    pipeline = [{"$match": {"chatbot.qnid": {"$exists": True},
                            "created_at": {"$gte": make_timezone_aware(start),
                                           "$lte": make_timezone_aware(end)}}},
                {"$group": {"_id": "$chatbot.qnid",
                            "count": {"$sum": 1}}},
                {"$lookup": {"from": "question",
                             "localField": "_id",
                             "foreignField": "_id",
                             "as": "question"}},
                {"$sort": SON([("count", -1)])},
                {"$unwind": {"path": "$question",
                             "preserveNullAndEmptyArrays": False}},
                {"$replaceRoot": {"newRoot": {"_id": "$_id",
                                              "count": "$count",
                                              "text": f"$question.text.{language}"}}}]
    res = []
    async for item in message_collection.aggregate(pipeline):
        res.append(QuestionRankingDataModel(**common_helper(item)))
    return res


async def top_topics_of_week(today: datetime):
    pipeline = [{"$match": {"created_at": {"$gte": make_timezone_aware(today) - timedelta(days=7),
                                           "$lte": make_timezone_aware(today)},
                            "handler": "bot"}},
                {"$lookup": {"from": "question",
                             "localField": "chatbot.qnid",
                             "foreignField": "_id",
                             "as": "question"
                             }},
                {"$unwind": {"path": "$question", "preserveNullAndEmptyArrays": False}},
                {"$group": {"_id": "$question.topic", "count": {"$sum": 1.0}}},
                {"$sort": SON([("count", -1)])}]
    res = []
    async for item in message_collection.aggregate(pipeline):
        res.append(common_helper(item))
    return res


async def get_word_cloud(today: datetime):
    pipeline = [{"$match": {"created_at": {"$gte": make_timezone_aware(today) - timedelta(days=7),
                                           "$lte": make_timezone_aware(today)},
                            "handler": "bot"}},
                {"$addFields": {"words": {"$map": {"input": {"$split": ["$data.text", " "]},
                                                   "as": "str",
                                                   "in": {"$trim": {"input": {"$toLower": ["$$str"]},
                                                                    "chars": " ,|(){}-<>.;"}}}}}},
                {"$unwind": {"path": "$words", "preserveNullAndEmptyArrays": False}},
                {"$match": {"words": {"$nin": default_stop_words}}},
                {"$group": {"_id": "$words", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1)])},
                {"$limit": 80}]
    res = []
    async for item in message_collection.aggregate(pipeline):
        res.append(common_helper(item))
    return res
