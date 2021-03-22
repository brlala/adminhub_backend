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
    URL = 'web_url'
    FLOW = 'flow'
    POSTBACK = 'postback'
    PHONE = 'phone_number'

    # deprecated
    ELEMENT_SHARE = 'element_share'


class QuickReplyPayload(BaseModel):
    flow_id: Optional[str] = Field(alias='flowId')
    params: Optional[list[str]]


class QuickReplyItem(BaseModel):
    text: dict
    payload: Union[QuickReplyPayload, str]
    value: Optional[str]


class QuickReplyComponentSaveTo(BaseModel):
    attribute_name: Optional[str] = Field(alias='attributeName')
    is_temporary: Optional[bool] = Field(alias='isTemporary')


class QuickReplyComponent(BaseModel):
    quick_replies: Optional[list[QuickReplyItem]] = Field(alias='quickReplies')
    save_to: Optional[QuickReplyComponentSaveTo] = Field(alias='saveTo')


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


class AttachmentItemComponent(BaseModel):
    attachments: Optional[list[AttachmentItem]]
    url: Optional[str]


class GenericTemplateComponent(BaseModel):
    elements: Optional[list[GenericTemplateItem]]


class TextComponent(BaseModel):
    text: Optional[dict]


class FlowFlow(BaseModel):
    flow_id: Optional[str] = Field(alias='flowId')
    params: Optional[list[str]]


class FlowComponent(BaseModel):
    flow: Optional[FlowFlow]


class ButtonTemplateComponent(BaseModel):
    text: Optional[dict]
    title: Optional[dict]
    buttons: Optional[list[ButtonItem]]


class InputComponent(BaseModel):
    input_name: Optional[str] = Field(alias='inputName')
    input_type: Optional[str] = Field(alias='inputType')
    custom_regex: Optional[str] = Field(alias='customRegex')
    invalid_message: Optional[str] = Field(alias='invalidMessage')
    is_temporary: Optional[bool] = Field(alias='isTemporary')


class FunctionComponent(BaseModel):
    function: Optional[str]


class UserAttributeComponent(BaseModel):
    action_type: Optional[str] = Field(alias='actionType')
    attribute_name: Optional[str] = Field(alias='attributeName')
    attribute_value: Optional[str] = Field(alias='attributeValue')
    is_temporary: Optional[bool] = Field(alias='isTemporary')


class EntitySearchFilterEntity(BaseModel):
    user_attribute: Optional[str] = Field(alias='userAttribute')
    memory_attribute: Optional[str] = Field(alias='memoryAttribute')


class OperatorTypeEnum(str, Enum):
    MORE = '>'
    LESS = '<'
    EQUAL = '='
    NOT_EQUAL = '!='
    MORE_THAN_OR_EQUAL = '>='
    LESS_THAN_OR_EQUAL = '<='
    IN = 'in'
    CONTAINS = 'contains'


class EntitySearchFilter(BaseModel):
    attribute: str
    operator: OperatorTypeEnum
    value: Union[str, EntitySearchFilterEntity]


class EntitySearchSort(BaseModel):
    attribute: str
    direction: int


class EntitySearchSearch(BaseModel):
    primary_entity: Optional[str] = Field(alias='primaryEntity')
    filters: list[EntitySearchFilter]
    sort: list[EntitySearchSort]


class EntitySearchDisplay(BaseModel):
    configure: bool


class EntitySearchFoundFlow(BaseModel):
    function_name: Optional[str] = Field(alias='functionName')


class EntitySearchComponent(BaseModel):
    search: Optional[EntitySearchSearch]
    display_attribute_answer: Optional[str] = Field(alias='displayAttributeAnswer')
    show_filter_msg: Optional[bool] = Field(alias='showFilterMsg')
    show_sort_msg: Optional[bool] = Field(alias='showSortMsg')
    skip_selection_when_one_result: Optional[bool] = Field(alias='skipSelectionWhenOneResult')
    display: Optional[EntitySearchDisplay]
    found_flow: Optional[EntitySearchFoundFlow] = Field(alias='foundFlow')
    not_found_flow: Optional[EntitySearchFoundFlow] = Field(alias='notFoundFlow')


class FlowComponents(AttachmentItemComponent, GenericTemplateComponent, TextComponent, FlowComponent,
                     ButtonTemplateComponent, InputComponent, FunctionComponent,
                     UserAttributeComponent, EntitySearchComponent, QuickReplyComponent):
    pass


class FlowTypeEnum(str, Enum):
    GENERIC_TEMPLATE = 'genericTemplate'
    IMAGES = 'images'
    FILE = 'file'
    FILES = 'files'
    BUTTON_TEMPLATE = 'buttonTemplate'
    FLOW = 'flow'
    MESSAGE = 'message'
    VIDEOS = 'videos'
    INPUT = 'input'
    CUSTOM = 'custom'
    IMAGE = 'image'
    AUDIO = 'audios'
    VIDEO = 'video'

    # not supported yet
    USER_ATTRIBUTE = 'userAttribute'
    ENTITY_SEARCH = 'entitySearch'

    def __str__(self):
        if self.value == self.IMAGES:
            return 'images'
        elif self.value == self.VIDEOS:
            return 'videos'
        return stringcase.snakecase(self.value)


class FlowItem(BaseModel):
    type: FlowTypeEnum
    data: FlowComponents


class FlowItemCreateIn(BaseModel):
    name: Optional[str]
    flow: list[FlowItem]
    is_active: Optional[bool] = Field(alias='isActive')

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
                            ],
                            "saveTo": {
                                "attributeName": "epay_process",
                                "isTemporary": True
                            }
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
                            "flow": {
                                "flowId": "5e315217a38e6703b4d3f81d",
                                "params": [

                                ]
                            }
                        }
                    },
                    {
                        "type": "message",
                        "data": {
                            "text": {
                                "EN": "TEST"
                            }
                        }
                    },
                    {
                        "type": "input",
                        "data": {
                            "isTemporary": True,
                            "inputName": "agent_ic",
                            "inputType": "custom",
                            "customRegex": "^\\d{3}$",
                            "invalidMessage": "You have entered an invalid format, please try again (etc. 123):"
                        }
                    },
                    {
                        "type": "custom",
                        "data": {
                            "function": "display_agent_birthyears"
                        }
                    },
                    {
                        "type": "image",
                        "data": {
                            "url": "https://s3-ap-southeast-1.amazonaws.com/choy-san/flow-image-1554258915.png"
                        }
                    },
                    {
                        "type": "video",
                        "data": {
                            "url": "https://gelm2prod.oss-ap-southeast-3.aliyuncs.com/portal/ePolicy%20agents.mp4"
                        }
                    },
                    {
                        "type": "userAttribute",
                        "data": {
                            "actionType": "set",
                            "attributeName": "life_claim",
                            "attributeValue": "Living Assurance",
                            "isTemporary": True
                        }
                    },
                    {
                        "type": "entitySearch",
                        "data": {
                            "search": {
                                "primaryEntity": "5ecdf7db51cc76038ea56e11",
                                "filters": [
                                    {
                                        "attribute": "ba218205-e72c-4cad-8b78-b13afb492886",
                                        "operator": "=",
                                        "value": {
                                            "userAttribute": "epay_bank"
                                        }
                                    },
                                    {
                                        "attribute": "ba218205-e72c-4cad-8b78-b13afb492886",
                                        "operator": "=",
                                        "value": {
                                            "memoryAttribute": "epay_attribute-value=a79ab047-c889-4735-adb2-1841c1f5f9ee"
                                        }
                                    },
                                    {
                                        "attribute": "name",
                                        "operator": "contains",
                                        "value": "Bharu"
                                    }
                                ],
                                "sort": [
                                    {
                                        "attribute": "name",
                                        "direction": 1
                                    },
                                    {
                                        "attribute": "ee0438e6-8514-4ac2-ae07-81bb7309bdde",
                                        "direction": -1
                                    }
                                ]
                            },
                            "displayAttributeAnswer": "c4282f1c-4351-424f-9558-889eb50f7903",
                            "showFilterMsg": False,
                            "showSortMsg": False,
                            "skipSelectionWhenOneResult": False,
                            "display": {
                                "configure": False
                            },
                            "foundFlow": {"functionName": "epay_documents_other"},
                            "notFoundFlow": {}
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


class QuickReplyPayloadOut(QuickReplyPayload):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ButtonItemOut(ButtonItem):
    payload: Optional[Union[QuickReplyPayloadOut, str]]
    title: Optional[Union[str, dict]]
    subtitle: Optional[Union[str, dict]]

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
    title: Union[str, dict]
    subtitle: Optional[Union[str, dict]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class QuickReplyItemOut(QuickReplyItem):
    payload: Union[QuickReplyPayloadOut, str]
    text: Optional[Union[str, dict]]
    title: Optional[str]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class QuickReplyComponentSaveToOut(QuickReplyComponentSaveTo):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class QuickReplyComponentOut(QuickReplyComponent):
    quick_replies: Optional[list[QuickReplyItemOut]] = Field(alias='quickReplies')
    save_to: Optional[QuickReplyComponentSaveToOut] = Field(alias='saveTo')

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class AttachmentItemComponentOut(AttachmentItemComponent):
    attachments: Optional[list[AttachmentItemOut]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class GenericTemplateComponentOut(GenericTemplateComponent):
    elements: Optional[list[GenericTemplateItemOut]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class TextComponentOut(TextComponent):
    text: Optional[Union[str, dict]]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowFlowOut(FlowFlow):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowComponentOut(FlowComponent):
    flow: Optional[FlowFlowOut]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ButtonTemplateComponentOut(ButtonTemplateComponent):
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


class EntitySearchFilterEntityOut(EntitySearchFilterEntity):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EntitySearchFilterOut(EntitySearchFilter):
    value: Union[str, EntitySearchFilterEntityOut]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EntitySearchSortOut(EntitySearchSort):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EntitySearchSearchOut(EntitySearchSearch):
    filters: list[EntitySearchFilterOut]
    sort: list[EntitySearchSortOut]

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EntitySearchDisplayOut(EntitySearchDisplay):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EntitySearchFoundFlowOut(EntitySearchFoundFlow):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EntitySearchComponentOut(EntitySearchComponent):
    search: Optional[EntitySearchSearchOut]
    display: Optional[EntitySearchDisplayOut]
    found_flow: Optional[EntitySearchFoundFlowOut] = Field(alias='foundFlow')
    not_found_flow: Optional[EntitySearchFoundFlowOut] = Field(alias='notFoundFlow')

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class FlowComponentsOut(AttachmentItemComponentOut, GenericTemplateComponentOut, TextComponentOut, FlowComponentOut,
                        ButtonTemplateComponentOut, InputComponentOut, FunctionComponentOut,
                        UserAttributeComponentOut, EntitySearchComponentOut, QuickReplyComponentOut):
    pass


class FlowTypeEnumOut(str, Enum):
    GENERIC_TEMPLATE = 'generic_template'
    IMAGES = 'images'
    FILE = 'file'
    FILES = 'files'
    BUTTON_TEMPLATE = 'button_template'
    FLOW = 'flow'
    MESSAGE = 'message'
    VIDEOS = 'videos'
    INPUT = 'input'
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audios'
    CUSTOM = 'custom'

    # for conversation
    POSTBACK = 'postback'

    # not supported yet on portal
    USER_ATTRIBUTE = 'user_attribute'
    ENTITY_SEARCH = 'entity_search'
    STICKER = 'sticker'

    def __str__(self):
        if self.value == self.IMAGES:
            return 'images'
        elif self.value == self.VIDEOS:
            return 'videos'
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


class FlowResponse(BaseModel):
    data: FlowSchemaDbOut

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
