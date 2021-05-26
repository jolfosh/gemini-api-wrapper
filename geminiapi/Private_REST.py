import requests
import json
import base64
import hmac
import hashlib
import time, time

class PrivateSession():
    def __init__(self, gemini_key, gemini_secret, sandbox=False):
        if sandbox:
            self.base_url = 'https://api.sandbox.gemini.com'
        else:
            self.base_url = 'https://api.gemini.com'
        self.api_key = gemini_key
        self.api_secret = gemini_secret.encode()
    
    # Send POST request to gemini api
    def apiPost(self, url_end, payload=None):
        # If payload is empty, set to empty dict
        if payload is None:
            payload = {}
            
        self.post_url = self.base_url + url_end
        
        # Create payload entry for request and nonce
        payload['request'] = url_end
        payload['nonce'] = str(int(time.time() * 1000))
        
        self.b64 = base64.b64encode(json.dumps(payload).encode())
        self.signature = hmac.new(self.api_secret, self.b64, hashlib.sha384).hexdigest()
        
        post_headers = {'Content-Type': "text/plain",
                        'Content-Length': "0",
                        'X-GEMINI-APIKEY': self.api_key,
                        'X-GEMINI-PAYLOAD': self.b64,
                        'X-GEMINI-SIGNATURE': self.signature,
                        'Cache-Control': "no-chache" }
                        
        self.response = requests.post(self.post_url, headers=post_headers)
        return self.response.json()
        
    
    def newOrder(self, symbol, amount, price, side, order_type, min_amount=None, options=None, stop_price=None, account=None):
        payload = { 'symbol': symbol,
                    'amount': amount,
                    'price': price,
                    'side': side,
                    'type': order_type }
                    
        # Add optional entries
        if min_amount is not None:
            payload['min_amount'] = min_amount
        if options is not None:
            payload['options'] = options
        if stop_price is not None:
            payload['stop_price'] = stop_price
        if account is not None:
            payload['account'] = account
        
        return self.apiPost('/v1/order/new', payload)
        
        
    def cancelOrder(self, order_id, account=None):
        payload = { 'order_id': order_id }
        
        if account is not None:
            payload['account'] = account
            
        return self.apiPost('/v1/order/cancel', payload)
        
        
    def cancelAllOrders(self, account=None):
        if account is not None:
            payload = { 'account': account }
        else:
            payload = {}
            
        return self.apiPost('/v1/order/cancel/all', payload)
        
    def showBalances(self, account=None, currency=None):
        if account is not None:
            payload = { 'account': account }
        else:
            payload = {}
            
        if currency is not None:
            return self.apiPost('/v1/notionalbalances/{}'.format(currency))
        else:
            return self.apiPost('/v1/balances')
            
    #Add Transfers/Deposit/Withdraw etc.