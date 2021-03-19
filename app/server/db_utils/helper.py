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


def question_helper(question) -> dict:
    # return {
    #     **question,
    #     "id": str(question["_id"]),
    #     "created_by": str(question["created_by"]) if question.get('created_by') else None,
    #     "updated_by": str(question["updated_by"]) if question.get('updated_by') else None,
    #     "answers": clean_dict_helper(question["answers"]) if question.get('answers') else None
    # }
    return clean_dict_helper({
        **question,
        "id": str(question["_id"]),
    })
