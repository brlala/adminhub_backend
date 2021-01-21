from datetime import date
from re import escape

import stringcase
from bson import ObjectId, Regex

from app.server.db.collections import flow_collection as collection
from app.server.models.current_user import CurrentUserSchema
from app.server.models.flow import FlowSchemaDb, NewFlow
from app.server.utils.common import clean_dict_helper, form_query
from app.server.utils.timezone import get_local_datetime_now, make_timezone_aware


def flow_helper(flow) -> dict:
    results = {
        **flow,
        "id": str(flow["_id"]),
    }
    return clean_dict_helper(results)


async def get_flow_one(_id: str) -> FlowSchemaDb:
    query = {"_id": ObjectId(_id)}
    async for flow in collection.find(query):
        return FlowSchemaDb(**flow_helper(flow))


async def get_flows_and_count_db(*, current_page: int, page_size: int, sorter: str = None, flow_name: str,
                                 language: str, updated_at: list[date], triggered_counts: list[int]) -> (
        list[FlowSchemaDb], int):
    if updated_at:
        updated_at_start, updated_at_end = updated_at
    db_key = [(f"name", {"$ne": None}),
              (f"name", Regex(f".*{escape(flow_name)}.*", "i") if flow_name else ...),
              (f"triggered_count", {"$gte": triggered_counts[0],
                                    "$lte": triggered_counts[1]} if triggered_counts else ...),
              ("is_active", True),
              ("updated_at", {"$gte": make_timezone_aware(updated_at_start),
                              "$lte": make_timezone_aware(updated_at_end)} if updated_at else ...)]
    query = form_query(db_key)

    flows = await get_flows_db(current_page=current_page, page_size=page_size, sorter=sorter, query=query)
    total = await get_flows_count_db(query=query)
    return flows, total





async def get_flows_db(*, current_page: int, page_size: int, sorter: str = None, query: dict) -> list[FlowSchemaDb]:
    # always show the newest first
    sort = [("_id", -1)]
    if sorter:
        # [("answers", 1), ("bot_user_group", 1)]
        for s in sorter.split(','):
            order = s[:1]
            key = s[1:]
            if order == '+':
                sort = [(stringcase.snakecase(key), 1)]
            else:
                sort = [(stringcase.snakecase(key), -1)]

    cursor = collection.find(query, sort=sort)
    cursor.skip((current_page - 1) * page_size).limit(page_size)
    questions = []
    async for flow in cursor:
        questions.append(FlowSchemaDb(**flow_helper(flow)))
    return questions


async def get_flows_count_db(*, query: dict) -> int:
    count = collection.count_documents(query)
    return await count


async def get_flows_filtered_field_list(field=None):
    query, projection = get_flows_cursor(field)
    flows = []
    async for flow in collection.find(query, projection=projection):
        flows.append(flow_helper(flow))
    return flows


def get_flows_cursor(field=None):
    projection = None
    query = {"is_active": True, "name": {"$ne": None}}
    if field:
        projection = {f: 1 for f in field.split(',')}
    return query, projection


async def add_flows_to_db(flow: NewFlow, current_user: CurrentUserSchema):
    doc = {
        "updated_at": get_local_datetime_now(),
        "topic": flow.topic,
        "created_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "type": flow.type,
        "is_active": True,
        "created_by": ObjectId(current_user.userId),
        "flow": flow.flow_items
    }
    result = await collection.insert_one(doc)
    return result.inserted_id
