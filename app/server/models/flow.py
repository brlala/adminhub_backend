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
    title: dict
    type: ButtonTypeEnum
    payload: Optional[Union[QuickReplyPayload, str]]
    url: Optional[str]


class GenericTemplateItem(BaseModel):
    file_name: str = Field(alias='fileName')
    image_url: str = Field(alias='imageUrl')
    title: dict
    subtitle: dict
    buttons: list[ButtonItem]


class AttachmentItemComponent(BaseModel):  # include file, video, image component
    attachments: Optional[list[AttachmentItem]]


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


class FlowComponents(AttachmentItemComponent, GenericTemplateComponent, TextComponent, FlowComponent,
                     ButtonTemplateComponent, QuickReplyComponent):
    pass


class FlowTypeEnum(str, Enum):
    GENERIC_TEMPLATE = 'genericTemplate'
    IMAGE = 'imageAttachment'
    FILE = 'fileAttachment'
    BUTTON_TEMPLATE = 'buttonTemplate'
    FLOW = 'flow'
    MESSAGE = 'message'
    VIDEO = 'videoAttachment'

    def __str__(self):
        if self.value == self.IMAGE:
            return 'images'
        elif self.value == self.FILE:
            return 'files'
        elif self.value == self.VIDEO:
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


class FlowComponentsOut(AttachmentItemComponentOut, GenericTemplateComponentOut, TextComponentOut, FlowComponentOut,
                        ButtonTemplateComponentOut, QuickReplyComponentOut):
    pass


class FlowTypeEnumOut(str, Enum):
    GENERIC_TEMPLATE = 'generic_template'
    IMAGE = 'images'
    FILE = 'files'
    BUTTON_TEMPLATE = 'button_template'
    FLOW = 'flow'
    MESSAGE = 'message'
    VIDEO = 'videos'

    def __str__(self):
        if self.value == self.IMAGE:
            return 'imageAttachment'
        elif self.value == self.FILE:
            return 'fileAttachment'
        elif self.value == self.VIDEO:
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
