import sys, os
from sqlalchemy import and_, or_, select
from schemas import FullNewsDTO, NewsDTO, TagDTO
sys.path.insert(0,os.path.join(sys.path[0], '..'))
from models import News, Tag, TagNews
from database import session_factory
from datetime import datetime

class Services:
    @staticmethod
    def getNews():
          with session_factory() as session:
               query = (
               select(News))
               res = session.execute(query)
               result_orm = res.scalars().all()
               result_dto = [NewsDTO.model_validate(row, from_attributes=True) for row in result_orm]
               return result_dto

    @staticmethod
    def getNewsById(id):
          with session_factory() as session:
               query = (
               select(News)
               .filter(News.id == id)
               )
               res = session.execute(query)
               result_orm = res.scalars().all()
               result_dto = [FullNewsDTO.model_validate(row, from_attributes=True) for row in result_orm]
               return result_dto
          
    @staticmethod
    def getTagsByNews(id):
          with session_factory() as session:
               query = (
               select(Tag)
               .select_from(TagNews)
               .join(Tag, TagNews.idTag == Tag.id)
               .filter(TagNews.idNews == id)
               )
               res = session.execute(query)
               result_orm = res.scalars().all()
               result_dto = [TagDTO.model_validate(row, from_attributes=True) for row in result_orm]
               return result_dto
    
    @staticmethod
    def getNewsByTagId(id):
          with session_factory() as session:
               query = (
               select(News)
               .select_from(TagNews)
               .join(News, TagNews.idNews == News.id)
               .filter(TagNews.idTag == id)
               )
               res = session.execute(query)
               result_orm = res.scalars().all()
               result_dto = [NewsDTO.model_validate(row, from_attributes=True) for row in result_orm]
               return result_dto
          
    @staticmethod
    def search(search = '  ', dateFrom = datetime.strptime("01.01.2000 00:00", '%d.%m.%Y %H:%M'), dateTo = datetime.now()):
          with session_factory() as session:
               query = (
               select(News)
               .filter(or_(News.text.contains(search), News.anons.contains(search), News.title.contains(search)))
               .filter(and_(dateFrom <= News.datePub, News.datePub <= dateTo))
               )

               res = session.execute(query)
               result_orm = res.scalars().all()
               result_dto = [NewsDTO.model_validate(row, from_attributes=True) for row in result_orm]
               return result_dto   