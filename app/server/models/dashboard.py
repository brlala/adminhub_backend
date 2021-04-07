from pydantic.main import BaseModel


class QuestionRankingDataModel(BaseModel):
    id: str
    count: int
    text: str
