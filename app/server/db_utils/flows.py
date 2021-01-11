from datetime import datetime

from bson import ObjectId

from app.server.db.collections import flow_user_collection
from app.server.models.flow import FlowSchemaDb
from app.server.models.question import QuestionSchemaDb
from app.server.utils.common import clean_dict_helper


def flow_helper(flow) -> dict:
    results = {
        **flow,
        "id": str(flow["_id"]),
    }
    return clean_dict_helper(results)


async def get_flows_from_db(*, current_page: int, page_size: int, sorter: str = None, question_text: str,
                            language: str, topic: str, created_at: datetime) -> list[QuestionSchemaDb]:
    pass
    # sort = []
    # if sorter:
    #     # [("answers", 1), ("bot_user_group", 1)]
    #     for s in sorter.split(','):
    #         order = s[:1]
    #         key = s[1:]
    #         if order == '+':
    #             sort.append((stringcase.snakecase(key), 1))
    #         else:
    #             sort.append((stringcase.snakecase(key), -1))
    #
    # db_key = [("topic", topic),
    #           (f"text.{language}", Regex(f".*{escape(question_text)}.*", "i") if question_text else None),
    #           ("created_at", created_at)]
    #
    # query = form_query(db_key)
    #
    # cursor = question_user_collection.find(query, sort=sort)
    # cursor.skip((current_page - 1) * page_size).limit(page_size)
    # questions = []
    # async for question in cursor:
    #     questions.append(QuestionSchemaDb(**flow_helper(question)))
    # return questions


async def get_flow_from_db(_id: str) -> FlowSchemaDb:
    query = {"_id": ObjectId(_id)}
    async for flow in flow_user_collection.find(query):
        return FlowSchemaDb(**flow_helper(flow))
