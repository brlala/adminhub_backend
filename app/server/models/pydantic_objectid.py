from bson import ObjectId
from pydantic import BaseModel


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Question(BaseModel):
    hey: PyObjectId


print(Question(**{"hey": ObjectId("5fb4804f3c137c45a8f16a4e")}))
