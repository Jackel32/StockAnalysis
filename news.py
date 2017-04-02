import json
import sys
import demjson
import datetime

try:
    from urllib.request import Request, urlopen
except ImportError:  # python 2
    from urllib2 import Request, urlopen

class News:
   'Common base class for all stock news'
      
   totalNewsCount = 0

googleNewsKeyToFullName = {
     u'usg'      : u'ID',
     u'd'        : u'Date',
     u'tt'       : u'TimeStamp',
     u'sp'       : u'Analysis',
     u's'        : u'Source',
     u'u'        : u'URL',
     u't'        : u'Text',
 }

months = {  1 : "January",
            2 : "February",
            3 : "March",
            4 : "April",
            5 : "May",
            6 : "June",
            7 : "July",
            8 : "August",
            9 : "September",
            10 : "October",
            11 : "November",
            12 : "December"
}



def __init__(self, symbol, totalNewsCount):
   self.name = name
   self.symbol = symbol
   ##self.totalNewsCount = totalNewsCount

def buildNewsUrl(symbol, qs='&start=0&num=1000'):
   return 'http://www.google.com/finance/company_news?output=json&q=' \
      + symbol + qs

##def parseDate(symbol):
##   News_str = json.dumps(getNews(symbol))
##   newsResp = json.loads(News_str);
##   for n in range
    

def getDate():
   now = datetime.datetime.now()
   day = now.day
   
   month = now.month
   ##getMonth(month)
   
   year = now.year
   getYear(year)

   return month, year
   

def getMonth(month):
   return months[month]()

def getYear(year):
   return year

def requestNews(symbol):
   url = buildNewsUrl(symbol)
   print "url: ", url
   req = Request(url)
   resp = urlopen(req)
   content = resp.read()

   content_json = demjson.decode(content)

   totalNews = content_json['total_number_of_news']

   article_json = []
   news_json = content_json['clusters']
   for cluster in news_json:
      for article in cluster:
         if article == 'a':
            article_json.extend(cluster[article])

   return article_json

def totalNews(symbol):
     url = buildNewsUrl(symbol)
     req = Request(url)
     resp = urlopen(req)
     content = resp.read()
     content_json = demjson.decode(content)
     totalNewsCount = content_json['total_number_of_news']
     
     return totalNewsCount

def replaceNewsKeys(news):
     global googleNewsKeyToFullName
     NewsWithReadableKey = []
     for n in news:
         nReadableKey = {}
         for j in googleNewsKeyToFullName:
             if j in n:
                 nReadableKey[googleNewsKeyToFullName[j]] = n[j]
         NewsWithReadableKey.append(nReadableKey)
     return NewsWithReadableKey

def getNews(symbol):
    return replaceNewsKeys(requestNews(symbol));

