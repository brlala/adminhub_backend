from datetime import datetime
from typing import Optional, Union, Any

from pydantic import BaseModel

from app.server.models.flow import FlowComponentsOut, ButtonItemOut, FlowSchemaDbOut
from app.server.models.question import QuestionSchemaDb
from app.server.utils.common import to_camel


class MessageChatbot(BaseModel):
    convo_id: Optional[str]
    flow_id: Optional[str]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ButtonItemConversationOut(ButtonItemOut):
    title: Optional[Union[str, dict]]


class FlowComponentsConversationOut(FlowComponentsOut):
    title: Optional[Any]
    subtitle: Optional[Any]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MessageSchemaDb(BaseModel):
    id: str
    type: str
    data: FlowComponentsOut
    chatbot: Optional[MessageChatbot]
    platform: str
    incoming_message_id: Optional[str]
    sender_platform_id: Optional[str]
    receiver_platform_id: str
    is_broadcast: bool = False
    abbr: Optional[str]
    handler: Optional[str]
    sender_id: str
    receiver_id: str
    created_at: datetime

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ConversationMessageDisplay(BaseModel):
    message: str
    created_at: datetime

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MessageNlpMatchedQuestionsQuestion(BaseModel):
    score: float
    question_id: str
    question_text: str
    question_topic: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MessageNlpMatchedQuestions(BaseModel):
    matched_questions: list[MessageNlpMatchedQuestionsQuestion]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MessageNlp(BaseModel):
    nlp_response: MessageNlpMatchedQuestions

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class MessageGradingSchemaDb(MessageSchemaDb):
    nlp: Optional[MessageNlp]
    fullname: Optional[str]
    answer_flow: Optional[FlowSchemaDbOut]
    answer_question: Optional[QuestionSchemaDb]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GetMessagesTable(BaseModel):
    data: list[MessageSchemaDb]
    success: bool
    total: int


class GetGradingsTable(BaseModel):
    data: list[MessageGradingSchemaDb]
    success: bool
    total: int
