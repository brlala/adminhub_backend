from datetime import datetime

from bson import ObjectId

from app.server.db.collections import flow_collection as collection
from app.server.models.current_user import CurrentUserSchema
from app.server.models.flow import FlowSchemaDb, NewFlow
from app.server.utils.common import clean_dict_helper
from app.server.utils.timezone import get_local_datetime_now


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


async def get_flows_list() -> list[FlowSchemaDb]:
    query, projection = get_flows_cursor()
    flows = []
    async for flow in collection.find(query, projection=projection):
        flows.append(FlowSchemaDb(**flow_helper(flow)))
    return flows


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


async def add_flows_to_db(flow: NewFlow, current_user:CurrentUserSchema):
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
