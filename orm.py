from sqlalchemy import select
from database import sync_engine, session_factory
from models import News, Tag

class Orm:
    @staticmethod
    def createTables(base):
        sync_engine.echo = False
        base.metadata.drop_all(sync_engine)
        base.metadata.create_all(sync_engine)
        sync_engine.echo = True
    
    @staticmethod
    def bulkInsert(insertData):
         with session_factory() as session:
                session.add_all(insertData)
                session.flush()
                session.commit()
     
    @staticmethod
    def insert(insertData):
         with session_factory() as session:
                session.add(insertData)
                session.flush()
                session.commit()

    @staticmethod
    def updateNews(query, newItem):
         with session_factory() as session:
              item = session.query(News).filter(query).first()
              if item == None:
                   return
              item.id = newItem.id
              item.anons = newItem.anons
              item.title = newItem.title
              item.datePub = newItem.datePub
              item.url = newItem.url
              item.text = newItem.text
              item.isProcessedContent = newItem.isProcessedContent
              session.commit()
    
    @staticmethod
    def insertTag(tag):
        with session_factory() as session:
            item = session.query(Tag).filter(Tag.name == tag.name).first()
            if item != None:   
                 return item
            session.add(tag)
            session.commit()
            session.refresh(tag)
            return tag
         
    @staticmethod
    def filter(model, query):
         with session_factory() as session:
              return session.query(model).filter(query)
         
    @staticmethod
    def getAll(model):
        # Добавить пагинацию
        with session_factory() as session:
            query = select(model)
            result = session.execute(query)
            return result.scalars().all()


