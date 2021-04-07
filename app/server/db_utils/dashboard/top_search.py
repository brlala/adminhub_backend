from datetime import date

from bson import SON

from app.server.db.collections import message_collection
from app.server.db_utils.helper import common_helper
from app.server.models.dashboard import QuestionRankingDataModel
from app.server.utils.timezone import make_timezone_aware


def question_ranking_helper():



def get_questions(*, start: date = None, end: date = None, language):
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
