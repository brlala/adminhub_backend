import re
from datetime import datetime
from re import escape

from bson import ObjectId, Regex

from app.server.db.collections import (broadcast_template_collection as template_collection,
                                       broadcast_collection as collection, flow_collection, bot_user_collection)
from app.server.db_utils.bot_user import bot_user_basic_information_helper
from app.server.models.current_user import CurrentUserSchema
from app.server.models.broadcast import BroadcastTemplateSchemaDb, NewBroadcastTemplate, \
    BroadcastHistoryListSchemaDbOut, \
    BroadcastHistorySchemaDbOut, FlowComponentIn, FlowButtonsIn, BroadcastTemplateSchemaDbOut, BroadcastIn
from app.server.models.portal_user import PortalUserBasicSchemaOut
from app.server.utils.common import clean_dict_helper, form_query, add_user_pipeline, to_camel
from app.server.utils.timezone import get_local_datetime_now, get_local_now


def broadcast_template_helper(broadcast_template) -> dict:
    results = {
        **broadcast_template,
        "id": str(broadcast_template["_id"]),
    }
    return clean_dict_helper(results)


def broadcast_history_list_helper(broadcast) -> dict:
    results = {
        "created_by": user_basic_information_helper(broadcast["created_by"]),
        "status": 'Completed' if broadcast["total"] == broadcast["processed"] > 0 else (
            'Sending' if broadcast["total"] > broadcast["processed"] >= broadcast["sent"] > 0 else 'Scheduled'),
        "tags": broadcast["tags"],
        "exclude": broadcast["exclude"],
        "send_to_all": broadcast["send_to_all"],
        "send_at": broadcast["send_at"],
        "sent": broadcast["sent"],
        "processed": broadcast["processed"],
        "total": broadcast["total"],
        "id": str(broadcast["_id"]),
    }
    return clean_dict_helper(results)


def user_basic_information_helper(user: dict) -> PortalUserBasicSchemaOut:
    results = {
        "username": user["username"],
        "id": str(user["_id"]),
    }
    return clean_dict_helper(results)


def format_flow_out(flow):
    for item in flow:
        item['type'] = to_camel(item['type'])
    return flow


def broadcast_history_helper(broadcast) -> dict:
    results = {
        **broadcast,
        "created_by": user_basic_information_helper(broadcast["created_by"]),
        "status": 'Completed' if broadcast["total"] == broadcast["processed"] > 0 else (
            'Sending' if broadcast["total"] > broadcast["processed"] >= broadcast["sent"] > 0 else 'Scheduled'),
        "flow": format_flow_out(broadcast["flow"]["flow"]),
        "id": str(broadcast["_id"]),
        "failed": [bot_user_basic_information_helper(user) for user in broadcast['failed']],
        "targets": [bot_user_basic_information_helper(user) for user in broadcast['targets']]
    }
    return clean_dict_helper(results)


async def get_broadcast_template_one(_id: str) -> BroadcastTemplateSchemaDb:
    query = {"_id": ObjectId(_id)}
    broadcast_template = await template_collection.find_one(query)
    return BroadcastTemplateSchemaDb(**broadcast_template_helper(broadcast_template))


async def get_broadcast_templates_list(*, flow: list[str],
                                       intersect: bool) -> list[BroadcastTemplateSchemaDb]:
    db_key = [("flow", {'$all' if intersect else '$in': flow} if flow else ...),
              ("is_active", True)]
    query = form_query(db_key)

    broadcast_templates = []
    async for broadcast_template in template_collection.find(query):
        broadcast_templates.append(BroadcastTemplateSchemaDbOut(**broadcast_template_helper(broadcast_template)))
    return broadcast_templates


async def get_broadcast_templates_filtered_field_list(field=None) -> list[BroadcastTemplateSchemaDb]:
    query, projection = get_broadcast_template_cursor(field)
    broadcast_templates = []
    async for broadcast_template in template_collection.find(query, projection=projection):
        broadcast_templates.append(BroadcastTemplateSchemaDb(**broadcast_template_helper(broadcast_template)))
    return broadcast_templates


def get_broadcast_template_cursor(field=None):
    projection = None
    query = {"is_active": True}
    if field:
        projection = {f: 1 for f in field.split(',')}
    return query, projection


async def add_broadcast_template_db(broadcast_template: NewBroadcastTemplate, current_user: CurrentUserSchema) -> str:
    doc = {
        "updated_at": get_local_datetime_now(),
        "created_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "created_by": ObjectId(current_user.userId),
        "is_active": True,
        "platforms": broadcast_template.platforms,
        "flow": broadcast_template.flow,
        "name": broadcast_template.name
    }

    result = await template_collection.insert_one(doc)
    return f"Added {1 if result.acknowledged else 0} broadcast template."


async def update_broadcast_template_db(template_id: str,
                                       broadcast_template: NewBroadcastTemplate,
                                       current_user: CurrentUserSchema) -> str:
    doc = {
        "updated_at": get_local_datetime_now(),
        "updated_by": ObjectId(current_user.userId),
        "platforms": broadcast_template.platforms,
        "flow": broadcast_template.flow,
        "name": broadcast_template.name,
        "is_active": broadcast_template.is_active
    }
    result = await template_collection.update_one({"_id": ObjectId(template_id)}, {"$set": doc})
    return f"Updated {1 if result.acknowledged else 0} broadcast template."


async def delete_broadcast_template_db(template_id: str,
                                       current_user: CurrentUserSchema) -> str:
    result = await template_collection.update_one({"_id": ObjectId(template_id)}, {"$set": {"is_active": False}})
    return f"Updated {1 if result.acknowledged else 0} broadcast template."


async def validate_broadcast_template(broadcast_template: NewBroadcastTemplate, *, exclude: str = None) -> (bool, str):
    name = broadcast_template.name
    extra_filter = {"_id": {"$ne": ObjectId(exclude)}} if exclude else {}

    if await template_collection.find_one({"is_active": True, "name": broadcast_template.name, **extra_filter}):
        return False, f"Broadcast Template with name {name} exists."

    if duplicate := await template_collection.find_one({"is_active": True,
                                                        "flow": broadcast_template.flow, **extra_filter}):
        return False, f"Broadcast Template with same flow exists, named {duplicate['name']}."

    return True, ''


async def get_broadcast_history_list(*, tags: [], intersect: bool, status: str) -> list[BroadcastHistoryListSchemaDbOut]:
    db_key = [("tags", {'$all' if intersect else '$in': tags} if tags else ...),
              ("is_active", True)]
    query = form_query(db_key)
    user_pipeline = add_user_pipeline('created_by', 'created_by')
    pipeline = [{"$match": query}] + user_pipeline + [{"$sort": {"created_at": -1}}]
    broadcast_history = []
    async for broadcast in collection.aggregate(pipeline):
        if status == 'completed':
            if broadcast["total"] != broadcast["processed"]:
                continue
        elif status == 'sending':
            if (broadcast["total"] == broadcast["processed"]) or broadcast["processed"] == 0:
                continue
        elif status == 'scheduled':
            if broadcast["processed"] > 0:
                continue
        elif status == 'failed':
            continue
        broadcast_history.append(BroadcastHistoryListSchemaDbOut(**broadcast_history_list_helper(broadcast)))
    return broadcast_history


async def get_broadcast_history_one(_id) -> BroadcastHistorySchemaDbOut:
    query = {"_id": ObjectId(_id)}

    user_pipeline = add_user_pipeline('created_by', 'created_by')
    pipeline = [{"$match": query},
                {"$lookup": {"from": "bot_user", "localField": 'targets', "foreignField": "_id",
                             "as": "targets"}},
                {"$lookup": {"from": "bot_user", "localField": 'failed', "foreignField": "facebook.id",
                             "as": "failed"}}] + user_pipeline
    broadcast = await collection.aggregate(pipeline).next()
    return BroadcastHistorySchemaDbOut(**broadcast_history_helper(broadcast))


async def add_broadcast_db(broadcast: BroadcastIn, current_user: CurrentUserSchema) -> str:
    now = get_local_now()
    if broadcast.flowId:
        flow_id = broadcast.flowId
    else:
        doc = {
                "updated_at": now,
                "created_at": now,
                "updated_by": ObjectId(current_user.userId),
                "created_by": ObjectId(current_user.userId),
                "is_active": True,
                "platforms": broadcast.platforms,
                "flow": broadcast.dict(exclude_none=True, exclude_unset=True)['flow'],
                "type": "broadcast"
            }

        flow = await flow_collection.insert_one(doc)
        flow_id = flow.inserted_id

    if broadcast.sendToAll:
        bot_user_ids = await bot_user_collection.distinct('_id', {'is_active': True,
                                                                  "tags": {"$nin": broadcast.exclude}})
    else:
        bot_user_ids = await bot_user_collection.distinct('_id', {'is_active': True,
                                                                  "tags": {"$in": broadcast.tags,
                                                                           "$nin": broadcast.exclude}})

    doc = {
        "updated_at": now,
        "created_at": now,
        "updated_by": ObjectId(current_user.userId),
        "created_by": ObjectId(current_user.userId),
        "is_active": True,
        "platforms": broadcast.platforms,
        "flow_id": flow_id,
        "flow": await flow_collection.find_one(ObjectId(flow_id)),
        "tags": broadcast.tags,
        "exclude": broadcast.exclude,
        "send_to_all": broadcast.sendToAll,
        "targets": bot_user_ids,
        "send_at": datetime.strptime(broadcast.sendAt, '%Y-%m-%dT%H:%M:%S.%fZ') if broadcast.sendAt else now,
        "scheduled": broadcast.scheduled,
        "processed": 0,
        "sent": 0,
        "total": len(bot_user_ids)
    }

    result = await collection.insert_one(doc)
    return f"Added {1 if result.acknowledged else 0} broadcast template."


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
