import ssl
import websocket
import threading
import json
import pandas as pd
import numpy as np

class PublicWebSocket():
    def __init__(self, sandbox=False, make_log=False):
        if sandbox:
            self.base_url = 'wss://api.sandbox.gemini.com'
        else:
            self.base_url = 'wss://api.gemini.com'
        self.make_log = make_log
        self.v2 = False
        
    def _on_message(self, ws, message):
        def _run(*args):
            print(message)
            if self.make_log:
                json_message = json.loads(message)
                message_df = pd.json_normalize( json_message, 
                                                'events', 
                                                [
                                                    'type',
                                                    'eventId', 
                                                    'timestamp', 
                                                    'timestampms', 
                                                    'socket_sequence'
                                                ], 
                                                errors='ignore', 
                                                record_prefix='event_')                             
                message_df.to_csv(r'./csv/msg_log.csv', mode='a')                
        threading.Thread(target=_run).start()
        
    
    def _on_error(self, ws, error):
        print(error)
    
    def _on_close(self, ws, *args):
        print('### closed ###')
        
    def _on_open(self, ws):
        if self.v2:
            def open_run(*args):
                ws.send(self.json_payload)
            threading.Thread(target=_open_run).start()
        else:
            pass
         
    def _wsConnect(self, ws_url):
        def _connect_run(*args):
            self.ws = websocket.WebSocketApp(   ws_url, 
                                                on_message=self._on_message,
                                                on_error=self._on_error,
                                                on_close=self._on_close,
                                                on_open=self._on_open)
            self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        threading.Thread(target=_connect_run).start()
        
    def sendRequest(self, payload):
        json_payload = json.dumps(payload)
        def _req_run(*args):
            self.ws.send(json_payload)
            print("#########Add Subscription Request Sent!#########")
        threading.Thread(target=_req_run).start()
        
    def marketData_v1(self, symbol, heartbeat=False, top_of_book=False, bids=True, offers=True, trades=True, auctions=True):
        self.end_point = '/v1/marketdata/{}?heartbeat={}&top_of_book={}&bids={}&offers={}&trades={}&auctions={}'.format(symbol,heartbeat,top_of_book,bids,offers,trades,auctions)
        ws_url = self.base_url + self.end_point.lower()        
        self._wsConnect(ws_url)
        
    def marketData_v2(self, payload):    
        self.json_payload = json.dumps(payload)        
        end_point = '/v2/marketdata'
        ws_url = self.base_url + end_point        
        self._wsConnect(ws_url)
        
    def marketData_L2(self, symbols):
        self.v2 = True        
        payload = {"type":"subscribe",
                    "subscriptions":[{  "name":"l2",
                                        "symbols":symbols}]}
        self.marketData_v2(payload)
        
    def candleData(self, symbols, increment):
        self.v2 = True
        payload = { "type": "subscribe",
                    "subscriptions":[{  "name":"candles_{}".format(increment),
                                        "symbols":symbols}]}                                        
        self.marketData_v2(payload)
        
    def addSub(self, sub_name, symbols):
        payload = { "type": "subscribe",
                    "subscriptions":[{  "name":"{}".format(sub_name),
                                        "symbols":symbols}]}                       
        self.sendRequest(payload)
        
    def unSub(self, sub_name, symbols):
        payload = { "type": "unsubscribe",
                    "subscriptions":[{  "name":"{}".format(sub_name),
                                        "symbols":symbols}]}
        self.sendRequest(payload)
        
        
        