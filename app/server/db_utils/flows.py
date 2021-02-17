from datetime import date
from re import escape

import stringcase
from bson import ObjectId, Regex

from app.server.db.collections import flow_collection as collection
from app.server.models.current_user import CurrentUserSchema
from app.server.models.flow import FlowSchemaDb, NewFlow, FlowItemCreateIn, FlowItem, FlowTypeEnum, QuickReplyPayload, \
    FlowItemEditIn, FlowSchemaDbOut, FlowTypeEnumOut
from app.server.utils.common import clean_dict_helper, form_query, RequestMethod
from app.server.utils.timezone import get_local_datetime_now, make_timezone_aware


def flow_helper(flow) -> dict:
    for f in flow['flow']:
        f['type'] = str(FlowTypeEnumOut(f['type']))
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
    flows = []
    async for flow in cursor:
        flows.append(FlowSchemaDbOut(**flow_helper(flow)))
    return flows


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


async def add_flows_to_db_from_question(flow: NewFlow, current_user: CurrentUserSchema):
    """
    From question page, there is a similar method for flow page add_flows_to_db_from_flow
    """
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


async def add_flows_to_db_from_flow(flows_created: FlowItemCreateIn, current_user: CurrentUserSchema):
    """
    From Flow Page, there is a similar method for flow page add_flows_to_db_from_question
    """
    doc = await process_flow(flows_created, current_user, method=RequestMethod.ADD)
    result = await collection.insert_one(doc)
    return f"Added {1 if result.acknowledged else 0} flow."


def format_flow_to_database_format(flow: FlowItem):
    if flow.type == FlowTypeEnum.GENERIC_TEMPLATE:
        pass
    elif flow.type == FlowTypeEnum.IMAGE:
        pass
    elif flow.type == FlowTypeEnum.FILE:
        pass
    elif flow.type == FlowTypeEnum.VIDEO:
        pass
    elif flow.type == FlowTypeEnum.BUTTON_TEMPLATE:
        pass
    elif flow.type == FlowTypeEnum.FLOW:
        pass
    elif flow.type == FlowTypeEnum.MESSAGE:
        pass
    flow.type = str(flow.type)
    return convert_flow_buttons_to_object_id(flow)


def convert_flow_buttons_to_object_id(flow: FlowItem):
    # QR
    if flow.data.quick_replies:
        for qr in flow.data.quick_replies:
            if isinstance(qr.payload, QuickReplyPayload):
                qr.payload.flow_id = ObjectId(qr.payload.flow_id)

    # buttons
    if flow.data.elements:
        for elem in flow.data.elements:
            for b in elem.buttons:
                if isinstance(b.payload, QuickReplyPayload):
                    b.payload.flow_id = ObjectId(b.payload.flow_id)

    # flow
    if flow.data.flow_id:
        flow.data.flow_id = ObjectId(flow.data.flow_id)
    return flow.dict(exclude_none=True)


async def remove_flow_db(flow_ids: list[str], current_user: CurrentUserSchema) -> str:
    query = {"_id": {"$in": [ObjectId(f) for f in flow_ids]}, "is_active": True}

    set_query = {
        "updated_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "is_active": False
    }
    result = await collection.update_many(query, {'$set': set_query})

    return f"Removed {result.modified_count} flows."


async def process_flow(flow: FlowItemCreateIn, current_user, *, method: RequestMethod):
    doc = {
        "name": flow.name,
        "updated_at": get_local_datetime_now(),
        "created_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "type": 'storyboard',
        "is_active": True,
        "created_by": ObjectId(current_user.userId),
        "flow": [format_flow_to_database_format(f) for f in flow.flow]
    }

    if method == RequestMethod.EDIT:
        keys_to_remove = ["created_at", "created_by"]
        for key in keys_to_remove:
            doc.pop(key)
    return doc


async def edit_flow_db(flow: FlowItemEditIn, current_user: CurrentUserSchema):
    doc = await process_flow(flow, current_user, method=RequestMethod.EDIT)
    new_values = {"$set": doc}
    result = await collection.update_one({"_id": ObjectId(flow.id)}, new_values)
    return f"Updated {result.modified_count} question."
