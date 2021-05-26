import ssl
import websocket
import json
import base64
import hmac
import hashlib
import time
import threading

class PrivateWebSocket():
    def __init__(self, gemini_key, gemini_secret, sandbox=False):
        if sandbox:
            self.base_url = 'wss://api.sandbox.gemini.com'
        else:
            self.base_url = 'wss://api.gemini.com'
            
        self.message_count = 0
        self.api_key = gemini_key
        self.api_secret = gemini_secret.encode()
        
    def on_message(self, ws, message):
        def run(*args):
            print(message)
            self.message_count += 1
        threading.Thread(target=run).start()
        
    def on_error(self, ws, error):
        print(error)
        
    def on_close(self, ws):
        print('### session closed ###')

    def orderEvents(self, symbolFilter=None, apiSessionFilter=None, eventTypeFilter=None, heartbeat=True):
        self.url_end = '/v1/order/events'
        self.filters = False
        
        if symbolFilter is not None:
            if self.filters == False:
                self.filters = True
                self.url_end += '?'
            else: 
                self.url_end += '&'
            self.url_end += 'symbolFilter={}'.format('&symbolFilter='.join(symbolFilter))

        if apiSessionFilter is not None:
            if self.filters == False:
                self.filters = True
                self.url_end += '?'
            else: 
                self.url_end += '&'
            self.url_end += 'apiSessionFilter={}'.format('&apiSessionFilter='.join(apiSessionFilter))
            
        if eventTypeFilter is not None:
            if self.filters == False:
                self.filters = True
                self.url_end += '?'
            else: 
                self.url_end += '&'
            self.url_end += 'eventTypeFilter={}'.format('&eventTypeFilter='.join(eventTypeFilter))
        if heartbeat:
            if self.filters == False:
                self.filters = True
                self.url_end += '?heartbeat=true'
            else:
                self.url_end += '&heartbeat=true'
        self.ws_url = self.base_url + self.url_end
        
        self.payload = { 'request': '/v1/order/events',
                    'nonce': int(time.time()*1000) }
                    
        self.encoded_payload = json.dumps(self.payload).encode()
        self.b64 = base64.b64encode(self.encoded_payload)
        self.signature = hmac.new(self.api_secret, self.b64, hashlib.sha384).hexdigest()
        
        self.ws = websocket.WebSocketApp(self.ws_url, 
                                    on_message=self.on_message,
                                    header = {  'X-GEMINI-PAYLOAD': self.b64.decode(),
                                                'X-GEMINI-APIKEY': self.api_key,
                                                'X-GEMINI-SIGNATURE': self.signature })
        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})