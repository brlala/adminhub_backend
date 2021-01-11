from pydantic.main import BaseModel


class BotPortalSchemaDb(BaseModel):
    allowed_origin: list[str]
    region: str


class BotSchemaDb(BaseModel):
    id: str
    name: str
    abbreviation: str
    portal: BotPortalSchemaDb

class BotSchemaDbOut(BotSchemaDb):
    pass
