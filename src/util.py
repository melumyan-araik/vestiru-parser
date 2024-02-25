from datetime import datetime, timedelta, timezone
import locale

def dateParseToUTC(date_str):
    locale_sys = locale.getlocale()
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
    d = datetime.strptime(date_str,'%d %m %YT%H:%M')
    mskDelta = timedelta(hours=3)
    d -= mskDelta
    locale.setlocale(locale.LC_ALL, locale_sys)
    return datetime(d.year, d.month, d.day, d.hour, d.minute, 0, 0, tzinfo=timezone(timedelta(0)))

def monthToNumber(str):
    monthList = ['янв', 'фев', 'мар', 'апр', 'ма', 'июн',
           'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
    listdate = str.split()
    month = listdate[1].lower()
    for i in range(0, len(monthList)):
        if monthList[i] in month:
            month = i+1
            break
    return f"{listdate[0]} {month} {listdate[2]}"