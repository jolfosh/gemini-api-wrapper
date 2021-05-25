# Gemini API Wrapper
 Python API Wrapper for easier Gemini Trading

For more information on how the API works, check out the [Gemini API Docs](https://docs.gemini.com/rest-api/).



### Public REST

##### Import Header

```python
from gemini import Public_REST as pubR
```



##### Declare Public Session

```python
sandbox = False

r = pR.PublicSession(sandbox)
```



##### Methods

```python
#	Methods return the response from GET request

r.getSymbols()

r.getPriceFeed()

r.getBook(symbol='btcusd')

r.getSymbolDetails(symbol='btcusd')

r.getTicker(symbol='btcusd')

r.getTickerV2(symbol='btcusd')

r.getCandles(	
    			symbol='btcusd', 
             	time_frame='5m'			#optional
            )

r.getTradeHistory(	
    				symbol='btcusd', 
                  	timestamp='', 		#optional 
                  	limit_trades=''		#optional
                 	include_breaks=''	#optional
                 )	


#COMING SOON:
r.getCurrentAuction()
r.getAuctionHistory()
```



### Private REST



##### Import Header

``` python
from gemini import Private_REST as privR
```



##### Declare Private Session

```python
sandbox=False

p = privR.PrivateSession(gemini_api_key, gemini_api_secret, sandbox)
```



##### Methods

```python
#	Methods return the response from POST request

p.newOrder(	
    		symbol='btcusd',				#required
           	amount='1', 					#required
          	price='30145.01', 				#required
          	side='buy', 					#required
          	order_type = 'exchange_limit',	#required
          	min_amount = '1',				#optional
           	options = '', 					#optional
           	stop_price = '30145.01'			#optional
           	account = ''					#optional
          )

p.cancelOrder(	
    			order_id='12345', 
              	account=''			#optional
             )

p.cancelAllOrders(	
    				account='' 		#optional
                 )

p.showBalances(
    			account='',			#optional
              	currency=''			#optional
              )

'''
Coming Soon:
Functions for Transfer/Deposit/Withdraw etc.
'''
```