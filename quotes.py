import json
import demjson
import urllib
import urllib2

try:
    from urllib.request import Request, urlopen
except ImportError:  # python 2
    from urllib2 import Request, urlopen

class Quotes:
    'Common base class for all stock quotes'

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


def __init__(self, symbols):
  self.name = name
  self.symbols = symbols

def buildQuoteURL(symbols):
    symbol_list = ','.join([symbol for symbol in symbols])
    # a deprecated but still active & correct api
    symbol_list = urllib.quote(symbol_list)
    return 'http://finance.google.com/finance/info?client=ig&q=' + symbol_list


def requestQuote(symbols):
    url = buildQuoteURL(symbols)
    req = Request(url)
    resp = urlopen(req)
    # remove special symbols such as the pound symbol
    ##content = resp.read().decode("ascii", "ignore").strip()

    content = resp.read()##.decode("ascii", "ignore").strip()
    
    content = content[3:]
    
    #f = open('output.txt','w')
    #print >> f, content
    
    return content

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
    if type(symbols) == type("str"):
        symbols = [symbols]
        
    content = json.loads(requestQuote(symbols));

    ##f = open('output.txt','w')
    ##print >> f, content
    
    return replaceQuoteKeys(content);
