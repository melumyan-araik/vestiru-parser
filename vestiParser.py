import os
from dotenv import load_dotenv
load_dotenv()
import json
import requests
from orm import Orm
from models import News, Base, Tag, TagNews
from database import createDB
from util import dateParseToUTC, monthToNumber
from bs4 import BeautifulSoup as bs
import schedule

class VestiParser:
    def __init__(self, isCreateDb, isCreateTable): 
        self.isCreateDb = isCreateDb
        self.isCreateTable = isCreateTable     
        self.url = os.getenv("BASE_URL")
        if self.isCreateDb:
            createDB()
        if self.isCreateTable:
            Orm.createTables(Base)

    def start(self):
         self.mainInfoParse()
         self.contentInfoParse
         schedule.every(60).minutes.do(self.mainInfoParse)
         schedule.every(40).minutes.do(self.contentInfoParse)
         while True:
            schedule.run_pending()

    def contentInfoParse(self):
        rawListNews = Orm.filter(News, News.isProcessedContent==False).all()

        for item in rawListNews:
            print(f"=========================")
            print(f"{self.url}{item.url}")
            req = requests.get(f"{self.url}{item.url}").text 
            soup = bs(req, 'lxml')
            listP = soup.find("div", class_="js-mediator-article").find_all('p')
            text = ""
            for p in listP:
                text += p.text
            item.text = text
            item.isProcessedContent = True
            Orm.updateNews(News.id == item.id, item)

            listTags = soup.find("div", class_="tags").find_all("a")
            listT = []
            for tag in listTags:
                listT.append(Orm.insertTag(Tag(name=tag.text)))
            listTagNews = []
            for t in listT:
                listTagNews.append(TagNews(idNews=item.id, idTag=t.id))
            Orm.bulkInsert(listTagNews)
    
    def mainInfoParse(self):
        req = requests.get(f"{self.url}/api/news?page=1").text   
        reqJson = json.loads(req)
     
        if not reqJson["success"]:
            print("Неудачный запрос")
            return
        
        insertData = []
        for item in reqJson["data"]:
            insertData.append(News(
                 title=item["title"],
                 anons=item["anons"],
                 datePub= dateParseToUTC(monthToNumber(item["datePub"]["day"])+"T"+ item["datePub"]["time"]),
                 url=item["url"],
                 text="",
                 isProcessedContent= False
            ))
        Orm.bulkInsert(insertData)