import json
import sys
import demjson

try:
    from urllib.request import Request, urlopen
except ImportError:  # python 2
    from urllib2 import Request, urlopen

googleFinanceKeyToFullName = {
    u'id'       : u'ID',
    u't'        : u'StockSymbol',
    u'e'        : u'Index',
    u'l'        : u'LastTradePrice',
    u'l_cur'    : u'LastTradeWithCurrency',
    u'ltt'      : u'LastTradeTime',
    u'lt_dts'   : u'LastTradeDateTime',
    u'lt'       : u'LastTradeDateTimeLong',
    u'div'      : u'Dividend',
    u'yld'      : u'Yield',
    u's'        : u'LastTradeSize',
    u'c'        : u'Change',
    u'c'        : u'ChangePercent',
    u'el'       : u'ExtHrsLastTradePrice',
    u'el_cur'   : u'ExtHrsLastTradeWithCurrency',
    u'elt'      : u'ExtHrsLastTradeDateTimeLong',
    u'ec'       : u'ExtHrsChange',
    u'ecp'      : u'ExtHrsChangePercent',
    u'pcls_fix' : u'PreviousClosePrice',
    u'hi52'     : u'52 Week High',
    u'lo52'     : u'52 Week Low'
}

googleNewsKeyToFullName = {
    u'usg'      : u'ID',
    u'd'        : u'Date',
    u'tt'       : u'TimeStamp',
    u'sp'       : u'Analysis',
    u's'        : u'Source',
    u'u'        : u'URL',
    u't'        : u'Text',
}

def buildQuoteURL(symbols):
    symbol_list = ','.join([symbol for symbol in symbols])
    # a deprecated but still active & correct api
    return 'http://finance.google.com/finance/info?client=ig&q=' \
        + symbol_list

def buildPreMarketURL(symbol, exchange=':NASDAQ'):
    return 'http://finance.google.com/finance/info?client=ig&q=' \
        + exchange + symbol
    ##return 'http://finance.google.com/finance/info?infotype=infoquoteall&q=' \
      ##     + exchange + symbol

def buildNewsUrl(symbol, qs='&start=0&num=100'):
   return 'http://www.google.com/finance/company_news?output=json&q=' \
        + symbol + qs

def requestQuote(symbols):
    url = buildQuoteURL(symbols)
    req = Request(url)
    resp = urlopen(req)
    # remove special symbols such as the pound symbol
    content = resp.read().decode('ascii', 'ignore').strip()
    content = content[3:]
    return content

def requestPreMarketQuote(symbols):
    url = buildPreMarketURL(symbols)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read()
    content = content[3:]
    return content

##def fetchPreMarket(symbol):
##    url = buildQuoteURL(symbols)
##    u = Request(url)
##    resp = urlopen(u)
##    content = resp.read()
##    data = json.loads(content[3:])
##    info = data[0]
##    t = str(info['elt'])    # time stamp
##    l = float(info["l"])    # close price (previous trading day)
##    p = float(info["el"])   # stock price in pre-market (after-hours)
##    hi = float(info["hi52"])
##    low = float(info["lo52"])
##    return (t,l,p,hi,low)

def requestNews(symbol):
    url = buildNewsUrl(symbol)
    print "url: ", url
    req = Request(url)
    resp = urlopen(req)
    content = resp.read()

    content_json = demjson.decode(content)

    ##print "total news: ", content_json['total_number_of_news']
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
    totalNews = content_json['total_number_of_news']
    
    return totalNews

def replaceQuoteKeys(quotes):
    global googleFinanceKeyToFullName
    quotesWithReadableKey = []
    for q in quotes:
        qReadableKey = {}
        for k in googleFinanceKeyToFullName:
            if k in q:
                qReadableKey[googleFinanceKeyToFullName[k]] = q[k]
        quotesWithReadableKey.append(qReadableKey)
    return quotesWithReadableKey

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

def getQuotes(symbols):
    '''
    get real-time quotes (index, last trade price, last trade time, etc) for stocks, using google api: http://finance.google.com/finance/info?client=ig&q=symbols
    Unlike python package 'yahoo-finance' (15 min delay), There is no delay for NYSE and NASDAQ stocks in 'googlefinance' package.
    example:
    quotes = getQuotes('AAPL')
    return:
    [{u'Index': u'NASDAQ', u'LastTradeWithCurrency': u'129.09', u'LastTradeDateTime': u'2015-03-02T16:04:29Z', u'LastTradePrice': u'129.09', u'Yield': u'1.46', u'LastTradeTime': u'4:04PM EST', u'LastTradeDateTimeLong': u'Mar 2, 4:04PM EST', u'Dividend': u'0.47', u'StockSymbol': u'AAPL', u'ID': u'22144'}]
    quotes = getQuotes(['AAPL', 'GOOG'])
    return:
    [{u'Index': u'NASDAQ', u'LastTradeWithCurrency': u'129.09', u'LastTradeDateTime': u'2015-03-02T16:04:29Z', u'LastTradePrice': u'129.09', u'Yield': u'1.46', u'LastTradeTime': u'4:04PM EST', u'LastTradeDateTimeLong': u'Mar 2, 4:04PM EST', u'Dividend': u'0.47', u'StockSymbol': u'AAPL', u'ID': u'22144'}, {u'Index': u'NASDAQ', u'LastTradeWithCurrency': u'571.34', u'LastTradeDateTime': u'2015-03-02T16:04:29Z', u'LastTradePrice': u'571.34', u'Yield': u'', u'LastTradeTime': u'4:04PM EST', u'LastTradeDateTimeLong': u'Mar 2, 4:04PM EST', u'Dividend': u'', u'StockSymbol': u'GOOG', u'ID': u'304466804484872'}]
    :param symbols: a single symbol or a list of stock symbols
    :return: real-time quotes list
    '''
    if type(symbols) == type('str'):
        symbols = [symbols]
    content = json.loads(requestQuote(symbols));
    return replaceQuoteKeys(content);

def getPreMarketQuote(symbols):
    if type(symbols) == type('str'):
        symbols = [symbols]
    content = json.loads(requestQuote(symbols));
    return content
    ##return replaceQuoteKeys(content);

def getNews(symbol):
    
    ##newsContent = requestNews(symbol)
    return replaceNewsKeys(requestNews(symbol));
    ##return requestNews(symbol);

if __name__ == '__main__':
    try:
        symbols = sys.argv[1]
    except:
        symbols = "GOOG,AAPL"

    symbols = symbols.split(',')

    total = totalNews("GOOG")

    ##hi, low = fetchPreMarket("GOOG")

    ##print(json.dumps(getNews("GOOG"), indent=2))
    ##print(json.dumps(getQuotes(symbols), indent=2))

    print(json.dumps(getPreMarketQuote(symbols), indent=2))

    News_str = json.dumps(getNews("GOOG"))
    newsResp = json.loads(News_str);

    Quote_str = json.dumps(getQuotes(symbols))
    quoteResp = json.loads(Quote_str);

    

    ##print(hi)
    ##print(low) 

    ## n in range(1, total):
     ##   print(newsResp[n]['Text'])
    ##print(quoteResp)      
