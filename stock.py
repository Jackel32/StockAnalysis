import json
import sys
import os
import codecs
from itertools import islice

import news
import quotes

def read_in_chunks(file_object, chunk_size):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    size = 0
    while True:
        
        data = file_object.read(chunk_size)
        print "Chunk length: " + str(len(data))
        if len(data) == 0:
            break
        elif len(data) % 16 != 0:
            data += ' ' * (16 - len(data) % 16)
        size += len(data)
        yield data

def get_line(filename):
        with open(filename) as file:
            for i in file:
                yield i

def parse_stocks(line, n, symbols):
    if n <= 0:
        return
    else:
        symbols += line
        print line, n, symbols
        parse_stocks(line, n-1, symbols)


        
##def buildPreMarketURL(symbol, exchange=':NASDAQ'):
##    return 'http://finance.google.com/finance/info?client=ig&q=' \
##        + exchange + symbol
##    ##return 'http://finance.google.com/finance/info?infotype=infoquoteall&q=' \
##      ##     + exchange + symbol
##


##def requestPreMarketQuote(symbols):
##    url = buildPreMarketURL(symbols)
##    req = Request(url)
##    resp = urlopen(req)
##    content = resp.read()
##    content = content[3:]
##    return content
##
####def fetchPreMarket(symbol):
####    url = buildQuoteURL(symbols)
####    u = Request(url)
####    resp = urlopen(u)
####    content = resp.read()
####    data = json.loads(content[3:])
####    info = data[0]
####    t = str(info['elt'])    # time stamp
####    l = float(info["l"])    # close price (previous trading day)
####    p = float(info["el"])   # stock price in pre-market (after-hours)
####    hi = float(info["hi52"])
####    low = float(info["lo52"])
####    return (t,l,p,hi,low)
##

##def getPreMarketQuote(symbols):
##    if type(symbols) == type('str'):
##        symbols = [symbols]
##    content = json.loads(requestQuote(symbols));
##    return content
##    ##return replaceQuoteKeys(content);
##

# Start with 0 size and empty symbols
# pull in 1k worth of data and parse it.
# empty size and symbols... rinse and repeat
#
#
#
def read_n_data(n, num_lines):
    symbols = ""
    while True:
        next_n_lines = list(islice(f, n))
        print next_n_lines
        count = 0
        if not next_n_lines:
            break
        for line in next_n_lines:
            #print line
            item = line.rstrip("\n\r");
            count = count + 1
            #print count
            if count == num_lines:
                symbols += item
            #elif line < count:
             #   print line
            else:
                symbols += item + ","
            #print symbols
            #parse_data(symbols)
        #symbols = ""
        print symbols
        #parse_data(symbols)
        yield symbols


def read_all_data(num_lines):
    symbols = ""
    for line in range(num_lines):
        item = f.readline();
        item = item.rstrip("\n\r");
        if line == num_lines:
            symbols += item
        else:
            symbols += item + ","
        
        #print item, len(item), line
    #print num_lines    
    #print symbols
    
    #symbols = symbols.split(",");
    #print symbols
    yield symbols

def parse_data(symbols):
    Quote_str = json.dumps(quotes.getQuotes(symbols), indent=2);
    f = open('output.txt','w')
    print >> f, Quote_str
    #print Quote_str


if __name__ == '__main__':
    try:
        symbols = sys.argv[1]
    except:
        filename = "symbols(TEST).data"

        num_lines = sum(1 for line in open(filename))
        with open(filename, 'r') as f:
            symbols = ""
            count = 0
            chunk = 2
            while count <= num_lines:
                count += chunk
                print count
                #symbols = read_data(num_lines)
                symbols = read_n_data(count, num_lines)
                #print symbols
                parse_data(symbols)




























        
##        num_lines = sum(1 for line in open(filename))
##        statinfo = os.stat(filename)
##        ##print statinfo.st_size
##
##        gen = get_line(filename)
##        lines_required = 2
##        line_count = 0
##        item = ""
##        num_lines = sum(1 for line in open(filename))
##        symbols = "";
##        print num_lines
##                
####        for line in open(filename):
####            
####            #parse_stocks(line,lines_required, symbols)
####            chunk = [next(gen) for i in range(lines_required)]
####            line_count += lines_required
####            if line_count < num_lines:
####                symbols += item;
####            else:
####                symbols += item + ",";
####            for piece in chunk:
####                symbols = "";
##                   #print piece
####                    #print size < statinfo.st_size
####                    #item = f.readline();
####                    #print size
####                    #item = item.rstrip("\n\r");
####                    #print item
####                if piece == num_lines:
####                    symbols += i;
####                else:
####                    symbols += i + ",";
##                #else:
##                    #print piece
##                    #print size < statinfo.st_size
##                    #item = f.readline();
##                    #print size
##                    #item = item.rstrip("\n\r");
##                    #print item
##                    #if piece == num_lines:
##                    #    symbols += item;
##                    #else:
##                    #    symbols += item + ",";
##
##        #num_lines = num_lines-6300
##        #print statinfo
##        with open(filename, 'r') as f:
##            symbols = "";
##            size = 0;
##            for piece in read_in_chunks(f, 1024):
##                symbols = "";
##                size = size + len(piece)
##                print size
##                print statinfo.st_size
##
##                if size <= statinfo.st_size:
##                    #print piece
##                    print size <= statinfo.st_size
##                    item = f.read();
##                    items = item.split(" ");
##                    print items
####                    #print size
##                    #item = item.rstrip("\n\r");
####                    #print item
##                    if piece <= 0:
##                        symbols += item;
##                    else:
##                        symbols += item + ",";
##                    print symbols
##                else:
##                    #print piece
##                    #print size < statinfo.st_size
##                    item = f.readline();
##                    #print size
##                    item = item.rstrip("\n\r");
##                    #print item
####                    if piece == num_lines:
####                        symbols += item;
####                    else:
####                        symbols += item + ",";
##                    #print "size is not working"
##                ##Quote_str = quotes.getQuotes(symbols);
##                ##print Quote_str
##                ##symbols = symbols.split(",");
##                ##print size
##                ##print symbols
##                ##Quote_str = json.dumps(quotes.getQuotes(symbols), indent=2);
##                ##print Quote_str
##                                
##        ##symbols = "GOOG,AAPL";
##        ##print symbols;
##
##    ##total = totalNews("GOOG")
##
##    ##hi, low = fetchPreMarket("GOOG")
##
##    ##print(json.dumps(getNews("GOOG"), indent=2))
##    ##print(json.dumps(getQuotes(symbols), indent=2))
##
##    ##print(json.dumps(getPreMarketQuote(symbols), indent=2))
##
##    ##total = news.totalNews("GOOG")
##    ##News_str = json.dumps(news.getNews("GOOG"))
##    ##newsResp = json.loads(News_str);
##
##    ##print quotes.getQuotes(symbols)
##
##    ##Quote_str = json.dumps(quotes.getQuotes(symbols), indent=2);
##    ##json_size = len(Quote_str)
##    ##serialized_size = len(serialized_object)
##    ##print json_size
##    ##f = open('output.txt','w')
##    ##print >> f, Quote_str
##    ##print Quote_str
##    ##quoteResp = json.loads(Quote_str);
##
##    
##
##    ##print(hi)
##    ##print(low) 
##    
##    ##print total
##    ##value = -1 * (100-total)
##
##    ##count = 0;
##    
##    ##for n in range(0, value):
##        ##news.parseDate()
##        ##print newsResp[n]#['Date'], "  --  ", news.getDate()
##        ##print n,": ", newsResp[n]['Date']#,newsResp[n]['Date'] 
##    ##print(quoteResp)      
