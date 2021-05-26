import requests
import json

class PublicSession():
    def __init__(self, sandbox=False):
        if sandbox:
            self.base_url = 'https://api.sandbox.gemini.com'
        else:
            self.base_url = 'https://api.gemini.com'
    
    def apiGET(self, end_point, url_params={}):
        self.response = requests.get(self.base_url + end_point, params=url_params)
        return self.response.json()
    
    
    def getSymbols(self):
        end_point = "/v1/symbols"
        return self.apiGET(end_point)

    def getSymbolDetails(self, symbol=None):
        if symbol is not None:
            end_point = "/v1/symbols/details/{}".format(symbol)
        else:
            print("Symbol Required. Please see list below")
            end_point = "/v1/symbols"
        return self.apiGET(end_point)
        
    def getTicker(self, symbol=None):
        end_point = "/v1/pubticker/{}".format(symbol)
        return self.apiGET(end_point)
        
    def getTickerV2(self, symbol=None):
        end_point = "/v2/ticker/{}".format(symbol)
        return self.apiGET(end_point)
        
    def getCandles(self, symbol=None, time_frame='5m'):
        end_point = "/v2/candles/{}/{}".format(symbol, time_frame)
        
    def getBook(self, symbol=None):
        end_point = "/v1/book/{}".format(symbol)
        return self.apiGET(end_point)
        
    def getTradeHistory(self, symbol='btcusd', timestamp=None, limit_trades=None, include_breaks=None):
        url_params = {  'timestamp' : timestamp,
                        'limit_trades' : limit_trades,
                        'include_breaks' : include_breaks }
        end_point = "/v1/trades/{}".format(symbol)
        return self.apiGET(end_point, url_params)
    
    def getPriceFeed(self):
        return self.apiGET("/v1/pricefeed")
    
    #ADD CURRENT_AUCTION AND AUCTION_HISTORY LATER