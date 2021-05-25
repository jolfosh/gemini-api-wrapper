import ssl
import websocket
import json
import base64
import hmac
import hashlib
import datetime, time

class PrivateWebSocket():
    def __init__(self, gemini_key, gemini_secret, sandbox=False):
        if sandbox:
            self.base_url = 'wss://api.sandbox.gemini.com'
        else:
            self.base_url = 'wss://api.gemini.com'
        
        self.api_key = gemini_key
        self.api_secret = gemini_secret.encode()
        
    def on_message(ws, message):
        print(message)
        
    def on_error(ws, error):
        print(error)
        
    def on_close(ws):
        print('### session closed ###')

    def initSession(self, symbolFilter=None, apiSessionFilter=None, eventTypeFilter=None, heartbeat=True):
        url_end = '/v1/order/events'
        filters = False
        
        if symbolFilter is not None:
            if filters == False:
                filters = True
                url_end += '?'
            else: 
                url_end += '&'
            url_end += 'symbolFilter={}'.format('&symbolFilter='.join(symbolFilter))

        if apiSessionFilter is not None:
            if filters == False:
                filters = True
                url_end += '?'
            else: 
                url_end += '&'
            url_end += 'apiSessionFilter={}'.format('&apiSessionFilter='.join(apiSessionFilter))
            
        if eventTypeFilter is not None:
            if filters == False:
                filters = True
                url_end += '?'
            else: 
                url_end += '&'
            url_end += 'eventTypeFilter={}'.format('&eventTypeFilter='.join(eventTypeFilter))
        if heartbeat:
            if filters == False:
                filters = True
                url_end += '?heartbeat=true'
            else:
                url_end += '&heartbeat=true'
        ws_url = self.base_url + url_end
        
        payload = { 'request': '/v1/order/events',
                    'nonce': int(time.time()*1000) }
                    
        encoded_payload = json.dumps(payload).encode()
        b64 = base64.b64encode(encoded_payload)
        signature = hmac.new(self.api_secret, b64, hashlib.sha384).hexdigest()
        
        ws = websocket.WebSocketApp(ws_url, 
                                    on_message=self.on_message,
                                    header = {  'X-GEMINI-PAYLOAD': b64.decode(),
                                                'X-GEMINI-APIKEY': self.api_key,
                                                'X-GEMINI-SIGNATURE': signature })
        ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})