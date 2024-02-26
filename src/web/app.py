import os
import sys
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

import uvicorn
from services import Services

app = FastAPI()

templates = Jinja2Templates(directory=os.path.join("templates"))

@app.get("/")
async def root(request: Request):
    listNews = Services.getNews()
    return templates.TemplateResponse("listNews.html", {"request": request, "listNews": listNews})

@app.get("/news/{id}")
def news(request: Request, id: int):
    news = Services.getNewsById(id)
    listTags = Services.getTagsByNews(id)
    return templates.TemplateResponse("news.html", {"request": request, "news": news[0], "listTags": listTags})

@app.get("/tag/{id}")
def newsByTag(request: Request, id: int):
    listNews = Services.getNewsByTagId(id)
    return templates.TemplateResponse("listNews.html", {"request": request, "listNews": listNews})

@app.post("/news/search")
async def search(request: Request,
    query: str | None  = Form(default=None),
    dateFrom : datetime | None = Form(default=None),
    dateTo: datetime | None = Form(default=None)):

    if query is None and dateFrom is None and dateTo is None:
        return RedirectResponse("/", status_code=303)
    
    listNews = []
    if query is not None:
        query = query.strip()
    if query is None:
        query = ' '
    if dateFrom is None:
        dateFrom = datetime.strptime("01.01.2000 00:00", '%d.%m.%Y %H:%M')
    if dateTo is None:
        dateTo = datetime.now()
        
    listNews = Services.search(query, dateFrom, dateTo)
    if len(listNews) == 0:
        return templates.TemplateResponse("noSearch.html", {"request": request, "query": query, "df": dateFrom, "dt": dateTo})
        
    return templates.TemplateResponse("listNews.html", {"request": request, "listNews": listNews})
