from  datetime import datetime
from pydantic import BaseModel

class NewsDTO(BaseModel):
    title: str
    anons: str
    datePub: datetime
    id: int

class FullNewsDTO(NewsDTO):
    text: str

class TagDTO(BaseModel):
    name: str
    id: int


