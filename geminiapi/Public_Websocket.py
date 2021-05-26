import ssl
import websocket
import threading

class PublicWebSocket():
    def __init__(self, sandbox=False):
        if sandbox:
            self.base_url = 'wss://api.sandbox.gemini.com'
        else:
            self.base_url = 'wss://api.gemini.com'
            
        self.message_count = 0    
        
    def on_message(self, ws, message):
        def run(*args):
            print(message)
            self.message_count += 1
        threading.Thread(target=run).start()
    
    def on_error(self, ws, error):
        return error
    
    def on_close(self, ws, *args):
        return '### closed ###'
        
    def marketData(self, symbol, heartbeat=False, top_of_book=False, bids=True, offers=True, trades=True, auctions=True):
        self.end_point='/v1/marketdata/{}?heartbeat={}&top_of_book={}&bids={}&offers={}&trades={}&auctions={}'.format(symbol,heartbeat,top_of_book,bids,offers,trades,auctions)
        self.ws_url = self.base_url + self.end_point.lower()
        
        self.ws = websocket.WebSocketApp(self.ws_url, on_message=self.on_message)
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})