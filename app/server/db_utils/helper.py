from app.server.models.flow import FlowTypeEnumOut
from app.server.utils.common import clean_dict_helper


def message_helper(message) -> dict:
    message['type'] = str(FlowTypeEnumOut(message['type']))
    return clean_dict_helper({
        **message,
        "id": str(message["_id"]),
    })


def bot_user_helper(bot_user) -> dict:
    return clean_dict_helper({
        **bot_user,
        "id": str(bot_user["_id"]),
        "last_message": message_helper(bot_user['last_message']) if bot_user.get('last_message') else None
    })
