import asyncio
from typing import Dict, Any
import websockets
import json

class HitBTC(object):
    # Link to the calling class
    parent = ""
    # JSON data returned from the web socket
    jsonData = {}  # type: Dict[Any, Any]
    # web soeck variable
    websocket = ""
    # ticker dictionary to track our trading pairs
    ticker = {'EOS': 0}
    # Multi layered candle dictionary for trend analysis
    candles = { 'EOS' :
                    { '15' :
                          { '1' : '1', '2' : '2', '3' : '3', '4' : '4'  }
                      }
                }

    def __init__(self, parent):

        # Save the reference to the calling object
        self.parent = parent

    async def connect(self):

        # Connect to the HitBTC websocket API
        async with websockets.connect('wss://api.hitbtc.com/api/2/ws') as self.websocket:

            # Subscribe to the EOSUSD ticker
            await self.websocket.send(
                '{"method": "subscribeTicker","params": {"symbol": "EOSUSD"},"id": 123}')

            # Subscribe to the ETHUSD ticker
            await self.websocket.send(
                '{"method": "subscribeTicker","params": {"symbol": "ETHUSD"},"id": 123}')

            # Subscribe to the 15 min candles for ETHUSD
            await self.websocket.send(
                '{"method": "subscribeCandles","params": {"symbol": "EOSUSD","period": "M15"},"id": 123}')

            # Loop for ever or until Ctl^c is hit
            while True:
                # Save the response to our JSON variable
                self.jsonData = await self.websocket.recv()

                # Convert the srting returned to JSON format
                self.jsonData = json.loads(self.jsonData)

                #Pass the JSON to the handler for handling
                self.handler(self.jsonData)

    def handler(self, json):

        # Check that the params key exists in our Dict
        if 'params' in json:

            '''if this is from the ticker method, pass to function update
             to be processed '''
            if self.jsonData['method'] == 'ticker': self.update_ticker(json['params'])


    def update_ticker(self, json: object) -> dict:

        try:
            self.ticker[json['symbol']] = json['last']
        except KeyError:
            self.ticker.update( { json['symbol'] : json['last'] } )
        except:
            pass

        print(self.ticker)

# Create a HitBTC object
h = HitBTC("test")
# Starting the async
asyncio.get_event_loop().run_until_complete(h.connect())
