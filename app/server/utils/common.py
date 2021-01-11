import stringcase
from bson import ObjectId


def without_keys(d, keys):
    """
    return a copy of dictionary without the keys specified
    invalid = {"keyA", "keyB"}
    without_keys(my_dict, invalid)
    :param d:
    :param keys:
    :return:
    """
    return {x: d[x] for x in d if x not in keys}


def with_keys(d, keys):
    """
    return a copy of dictionary without the keys specified
    invalid = {"keyA", "keyB"}
    only_keys(my_dict, invalid)
    :param d:
    :param keys:
    :return:
    """
    return {x: d[x] for x in d if x in keys}


def clean_dict_helper(d):
    if isinstance(d, ObjectId):
        return str(d)

    if isinstance(d, list):  # For those db functions which return list
        return [clean_dict_helper(x) for x in d]

    if isinstance(d, dict):
        for k, v in d.items():
            d.update({k: clean_dict_helper(v)})

    return d


def form_query(fields: list[tuple]) -> dict:
    query = {}
    for key, value in fields:
        if value is not ...:
            query[key] = value
    return query


def to_camel(string: str) -> str:
    return stringcase.camelcase(string)
