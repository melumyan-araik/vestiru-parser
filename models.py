import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, DeclarativeBase, mapped_column, Mapped
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    id: Mapped[intpk]
    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
class News(Base):
    title: Mapped[str]
    anons:  Mapped[str]
    datePub:  Mapped[datetime.datetime]
    url:  Mapped[str]
    text:  Mapped[str]
    isProcessedContent:  Mapped[bool]

class Tag(Base):
    name: Mapped[str] = mapped_column(unique=True)

class TagNews(Base):
    idNews: Mapped[int] = mapped_column(ForeignKey("news.id"))
    idTag: Mapped[int] = mapped_column(ForeignKey("tag.id"))

class LastStartParser(Base):
    lastStart: Mapped[datetime.datetime]
