from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class BotUserSchemaLastActive(BaseModel):
    received_at: datetime
    received_message_id: str
    sent_at: datetime
    sent_message_id: str


class BotUserSchemaFacebook(BaseModel):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]


class BotUserSchemaDb(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: Optional[str]
    gender: Optional[str]
    profile_pic_url: Optional[str]
    auth_flag: int
    is_broadcast_subscribed: bool
    last_active: BotUserSchemaLastActive
    bot_id: str
    bot_user_group_id: Optional[str]
    platforms: list[str]
    facebook: Optional[BotUserSchemaFacebook]
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    is_active: bool

    text: dict
    internal: bool
    keyword: Optional[list[str]]
    answers: list[QuestionAnswerSchema]
    alternate_questions: list[QuestionVariationSchema]
    topic: str
    active_at: Optional[datetime]
    expire_at: Optional[datetime]
    is_active: bool

    class Config:
        schema_extra = {
            "example": {
                "id": "5fe14e41d0c0a70910280174",
                "created_at": datetime.now(),
                "created_by": ObjectId("5e6217be51cc760b8677707e"),
                "updated_at": datetime.now(),
                "updated_by": ObjectId("5e6217be51cc760b8677707e"),
                "text": {
                    "EN": "Christmas e-card"
                },
                "internal": True,
                "keyword": ['a', 'b', 'c'],
                "answers": [
                    {
                        "id": "1",
                        "flow": {
                            "flow_id": ObjectId("5fe14d8dd0c0a7091028015c")
                        },
                        "bot_user_group": "1"
                    }
                ],
                "alternate_questions": [
                    {
                        "id": "a11b2322-e0e1-421c-b187-a96e1c9b4c37",
                        "text": "Merry Xmas greeting card",
                        "language": "EN",
                        "internal": False
                    },
                ],
                "topic": "Christmas e-Card",
                "active_at": None,
                "expire_at": None,
                "is_active": False
            }
        }
