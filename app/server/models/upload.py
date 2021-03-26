from pydantic import BaseModel


class UploadUrl(BaseModel):
    url: str
