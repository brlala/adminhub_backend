from datetime import datetime
from enum import Enum
from typing import Optional, Union

import stringcase
from pydantic import Field
from pydantic.main import BaseModel

from app.server.utils.common import to_camel


class FlowText(BaseModel):
    EN: Optional[str]


class FlowData(BaseModel):
    text: Optional[FlowText]


class AttachmentItem(BaseModel):
    file_name: str = Field(alias='fileName')
    url: str


class ButtonTypeEnum(str, Enum):
    url = 'web_url'
    flow = 'flow'
    postback = 'postback'


class QuickReplyPayload(BaseModel):
    flow_id: Optional[str] = Field(alias='flowId')
    params: Optional[list[str]]


class QuickReplyItem(BaseModel):
    text: dict
    payload: Union[QuickReplyPayload, str]


class ButtonItem(BaseModel):
    title: Optional[dict]
    type: ButtonTypeEnum
    payload: Optional[Union[QuickReplyPayload, str]]
    url: Optional[str]


class GenericTemplateItem(BaseModel):
    file_name: Optional[str] = Field(alias='fileName')
    image_url: Optional[str] = Field(alias='imageUrl')
    title: Optional[dict]
    subtitle: dict
    buttons: list[ButtonItem]


class AttachmentItemComponent(BaseModel):  # include file, video, image component
    attachments: Optional[list[AttachmentItem]]
    url: Optional[str]


class GenericTemplateComponent(BaseModel):  # include file, video, image component
    elements: Optional[list[GenericTemplateItem]]


class QuickReplyComponent(BaseModel):  # include file, video, image component
    quick_replies: Optional[list[QuickReplyItem]] = Field(alias='quickReplies')


class TextComponent(BaseModel):  # include file, video, image component
    text: Optional[dict]


class FlowComponent(BaseModel):  # include file, video, image component
    flow_id: Optional[str] = Field(alias='flowId')
    params: Optional[list[str]]


class ButtonTemplateComponent(BaseModel):  # include file, video, image component
    text: Optional[dict]
    title: Optional[dict]
    buttons: Optional[list[ButtonItem]]


class InputComponent(BaseModel):
    input_name: Optional[str]
    input_type: Optional[str]
    custom_regex: Optional[str]
    invalid_message: Optional[str]
    is_temporary: Optional[bool]


class FunctionComponent(BaseModel):
    function: Optional[str]


class UserAttributeComponent(BaseModel):
    action_type: Optional[str]
    attribute_name: Optional[str]
    attribute_value: Optional[str]
    is_temporary: Optional[bool]


class FlowComponents(AttachmentItemComponent, GenericTemplateComponent, TextComponent, FlowComponent,
                     ButtonTemplateComponent, QuickReplyComponent, InputComponent, FunctionComponent, UserAttributeComponent):
    pass


class FlowTypeEnum(str, Enum):
    GENERIC_TEMPLATE = 'genericTemplate'
    IMAGES = 'imageAttachment'
    FILE = 'fileAttachment'
    BUTTON_TEMPLATE = 'buttonTemplate'
    FLOW = 'flow'
    MESSAGE = 'message'
    VIDEOS = 'videoAttachment'

    # not supported yet
    INPUT = 'input'
    CUSTOM = 'custom'
    IMAGE = 'image'
    VIDEO = 'video'
    USER_ATTRIBUTE = 'userAttribute'
    ENTITY_SEARCH = 'entitySearch'

    def __str__(self):
        if self.value == self.IMAGES:
            return 'images'
        elif self.value == self.FILE:
            return 'files'
        elif self.value == self.VIDEOS:
            return 'videos'
        return stringcase.snakecase(self.value)


class FlowItem(BaseModel):
    type: FlowTypeEnum
    data: FlowComponents


class FlowItemCreateIn(BaseModel):
    name: Optional[str]
    flow: list[FlowItem]

    class Config:
        schema_extra = {
            "example": {
                "name": "new",
                "flow": [
                    {
                        "type": "genericTemplate",
                        "data": {
                            "elements": [
                                {
                                    "fileName": "test.png",
                                    "imageUrl": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/%E2%80%94Pngtree%E2%80%94futuristic%20circuit%20board%2Cillustration%20high%20computer_1071790.png",
                                    "title": {
                                        "EN": ""
                                    },
                                    "subtitle": {
                                        "EN": ""
                                    },
                                    "buttons": [
                                        {
                                            "title": {
                                                "EN": "button text1"
                                            },
                                            "type": "web_url",
                                            "url": "www.apple.com"
                                        }
                                    ]
                                },
                                {
                                    "buttons": [
                                        {
                                            "payload": {
                                                "flow_id": "5f6c2e46e3fbc4968da41d88",
                                                "params": [
                                                    "Bunny"
                                                ]
                                            },
                                            "title": {
                                                "EN": "Select"
                                            },
                                            "type": "postback"
                                        }
                                    ],
                                    "fileName": "",
                                    "imageUrl": "https://gelm2dev.oss-ap-southeast-3.aliyuncs.com/portal/flows/flow-attachment-1600888929-557.png",
                                    "subtitle": {
                                        "EN": "",
                                        "ZH": ""
                                    },
                                    "title": {
                                        "EN": "Bunny Greeting Card",
                                        "ZH": ""
                                    }
                                }
                            ],
                            "quickReplies": [
                                {
                                    "payload": {
                                        "flowId": "5f97a0833c137c45a8f162c2",
                                        "params": [

                                        ]
                                    },
                                    "text": {
                                        "EN": "IL PBEAR (U186)"
                                    }
                                },
                                {
                                    "payload": "Continue",
                                    "text": {
                                        "EN": "IL PBEAR (U186)"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "imageAttachment",
                        "data": {
                            "attachments": [
                                {
                                    "fileName": "test.pdf",
                                    "url": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/If%20You%20Suspect%20That%20You%20Are%20Infected%20With%20Covid-19%20%28210124TEH%29%20%281%29.pdf"
                                }
                            ]
                        }
                    },
                    {
                        "type": "fileAttachment",
                        "data": {
                            "attachments": [
                                {
                                    "fileName": "test.pdf",
                                    "url": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/If%20You%20Suspect%20That%20You%20Are%20Infected%20With%20Covid-19%20%28210124TEH%29%20%281%29.pdf"
                                }
                            ]
                        }
                    },

                    {
                        "type": "videoAttachment",
                        "data": {
                            "attachments": [
                                {
                                    "fileName": "test.mp4",
                                    "url": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/If%20You%20Suspect%20That%20You%20Are%20Infected%20With%20Covid-19%20%28210124TEH%29%20%281%29.mp4"
                                }
                            ]
                        }
                    },
                    {
                        "type": "buttonTemplate",
                        "data": {
                            "text": {
                                "EN": "TEST"
                            },
                            "buttons": [
                                {
                                    "title": {
                                        "EN": "button text1"
                                    },
                                    "type": "web_url",
                                    "content": {
                                        "EN": "www.apple.com"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "flow",
                        "data": {
                            "flowId": "5e315217a38e6703b4d3f81d",
                            "params": [

                            ]
                        }
                    },
                    {
                        "type": "message",
                        "data": {
                            "text": {
                                "EN": "TEST"
                            }
                        }
                    }
                ]
            }
        }


class FlowItemEditIn(FlowItemCreateIn):
    id: str

    class Config:
        schema_extra = {
            "example": {
                "id": "60235ffcb38bfe49acb97c3a",
                "name": "new",
                "flow": [
                    {
                        "type": "genericTemplate",
                        "data": {
                            "elements": [
                                {
                                    "fileName": "test.png",
                                    "imageUrl": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/%E2%80%94Pngtree%E2%80%94futuristic%20circuit%20board%2Cillustration%20high%20computer_1071790.png",
                                    "title": {
                                        "EN": ""
                                    },
                                    "subtitle": {
                                        "EN": ""
                                    },
                                    "buttons": [
                                        {
                                            "title": {
                                                "EN": "button text1"
                                            },
                                            "type": "web_url",
                                            "url": "www.apple.com"
                                        }
                                    ]
                                },
                                {
                                    "buttons": [
                                        {
                                            "payload": {
                                                "flow_id": "5f6c2e46e3fbc4968da41d88",
                                                "params": [
                                                    "Bunny"
                                                ]
                                            },
                                            "title": {
                                                "EN": "Select"
                                            },
                                            "type": "postback"
                                        }
                                    ],
                                    "fileName": "",
                                    "imageUrl": "https://gelm2dev.oss-ap-southeast-3.aliyuncs.com/portal/flows/flow-attachment-1600888929-557.png",
                                    "subtitle": {
                                        "EN": "",
                                        "ZH": ""
                                    },
                                    "title": {
                                        "EN": "Bunny Greeting Card",
                                        "ZH": ""
                                    }
                                }
                            ],
                            "quickReplies": [
                                {
                                    "payload": {
                                        "flowId": "5f97a0833c137c45a8f162c2",
                                        "params": [

                                        ]
                                    },
                                    "text": {
                                        "EN": "IL PBEAR (U186)"
                                    }
                                },
                                {
                                    "payload": "Continue",
                                    "text": {
                                        "EN": "IL PBEAR (U186)"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "imageAttachment",
                        "data": {
                            "attachments": [
                                {
                                    "fileName": "testasdasd.pdf",
                                    "url": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/If%20You%20Suspect%20That%20You%20Are%20Infected%20With%20Covid-19%20%28210124TEH%29%20%281%29.pdf"
                                }
                            ]
                        }
                    },
                    {
                        "type": "fileAttachment",
                        "data": {
                            "attachments": [
                                {
                                    "fileName": "testassas.pdf",
                                    "url": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/If%20You%20Suspect%20That%20You%20Are%20Infected%20With%20Covid-19%20%28210124TEH%29%20%281%29.pdf"
                                }
                            ]
                        }
                    },

                    {
                        "type": "videoAttachment",
                        "data": {
                            "attachments": [
                                {
                                    "fileName": "testasa.mp4",
                                    "url": "https://pandai-admin-portal.s3-ap-southeast-1.amazonaws.com/portal/flows/If%20You%20Suspect%20That%20You%20Are%20Infected%20With%20Covid-19%20%28210124TEH%29%20%281%29.mp4"
                                }
                            ]
                        }
                    },
                    {
                        "type": "buttonTemplate",
                        "data": {
                            "text": {
                                "EN": "TEST"
                            },
                            "buttons": [
                                {
                                    "title": {
                                        "EN": "button text1"
                                    },
                                    "type": "web_url",
                                    "content": {
                                        "EN": "www.apple.com"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "type": "flow",
                        "data": {
                            "flowId": "5e315217a38e6703b4d3f81d",
                            "params": [

                            ]
                        }
                    },
                    {
                        "type": "message",
                        "data": {
                            "text": {
                                "EN": "TEST"
                            }
                        }
                    }
                ]
            }
        }


# class ButtonItemOut(ButtonItem):
#     class Config:
#         alias_generator = to_camel
#         allow_population_by_field_name = True


class QuickReplyPayloadOut(QuickReplyPayload):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ButtonItemOut(ButtonItem):
    payload: Optional[Union[QuickReplyPayloadOut, str]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class AttachmentItemOut(AttachmentItem):
    file_name: Optional[str] = Field(alias='fileName')

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GenericTemplateItemOut(GenericTemplateItem):
    buttons: list[ButtonItemOut]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class QuickReplyItemOut(QuickReplyItem):
    payload: Union[QuickReplyPayloadOut, str]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class QuickReplyComponentOut(QuickReplyComponent):  # include file, video, image component
    quick_replies: Optional[list[QuickReplyItemOut]] = Field(alias='quickReplies')

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class AttachmentItemComponentOut(AttachmentItemComponent):  # include file, video, image component
    attachments: Optional[list[AttachmentItemOut]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GenericTemplateComponentOut(GenericTemplateComponent):  # include file, video, image component
    elements: Optional[list[GenericTemplateItemOut]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class TextComponentOut(TextComponent):  # include file, video, image component
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowComponentOut(FlowComponent):  # include file, video, image component
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ButtonTemplateComponentOut(ButtonTemplateComponent):  # include file, video, image component
    buttons: Optional[list[ButtonItemOut]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class InputComponentOut(InputComponent):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FunctionComponentOut(FunctionComponent):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

class UserAttributeComponentOut(UserAttributeComponent):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowComponentsOut(AttachmentItemComponentOut, GenericTemplateComponentOut, TextComponentOut, FlowComponentOut,
                        ButtonTemplateComponentOut, QuickReplyComponentOut, InputComponentOut, FunctionComponentOut, UserAttributeComponentOut):
    pass


class FlowTypeEnumOut(str, Enum):
    GENERIC_TEMPLATE = 'generic_template'
    IMAGES = 'images'
    FILE = 'files'
    BUTTON_TEMPLATE = 'button_template'
    FLOW = 'flow'
    MESSAGE = 'message'
    VIDEOS = 'videos'

    # not supported yet on portal
    INPUT = 'input'
    IMAGE = 'image'
    VIDEO = 'video'
    CUSTOM = 'custom'
    USER_ATTRIBUTE = 'user_attribute'
    ENTITY_SEARCH = 'entity_search'

    def __str__(self):
        if self.value == self.IMAGES:
            return 'imageAttachment'
        elif self.value == self.FILE:
            return 'fileAttachment'
        elif self.value == self.VIDEOS:
            return 'videoAttachment'
        return stringcase.camelcase(self.value)


class FlowItemOut(FlowItem):
    type: FlowTypeEnum
    data: FlowComponentsOut

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowSchemaDb(BaseModel):
    id: str
    created_at: datetime
    created_by: Optional[str]
    updated_at: datetime
    updated_by: Optional[str]
    topic: Optional[str]
    is_active: bool
    name: Optional[str]
    flow: list[FlowItem]
    type: str
    platforms: Optional[list[str]]
    params: Optional[list[str]]


class FlowSchemaDbOut(FlowSchemaDb):
    flow: list[FlowItemOut]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GetFlowsTable(BaseModel):
    data: list[FlowSchemaDbOut]
    success: bool
    total: int


class NewFlow(BaseModel):
    topic: str
    type: str
    flow_items: list[dict]


class DeleteFlows(BaseModel):
    key: list[str]

    class Config:
        schema_extra = {
            "example": {
                "key": ['6023502e837a202bee7d8e3e', '60235061837a202bee7d8e40']
            }
        }
