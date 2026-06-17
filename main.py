import requests          
import json
import time
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv() 

HEADERS={
    "APCA-API-KEY-ID" : os.getenv('ALPACA_API_KEY'),
    "APCA-API-SECRET-KEY" : os.getenv('ALPACA_SECRET_KEY')
}

BASE_URL = 'https://data.alpaca.markets/v2'
Quotes_URL = f"{BASE_URL}/stocks/SPY/quotes/latest"

end = datetime.now(timezone.utc)
start=end-timedelta(days=5)
Bars_URL=f"{BASE_URL}/stocks/SPY/bars"
params={
    "timeframe":"1Min",
    "start": start.isoformat(),
    "end": end.isoformat(),
    "feed":"iex"
}
response=requests.get(Bars_URL,headers=HEADERS,params=params)
if response.status_code!=200:
    raise SystemExit("Failed to load historical data")
data=response.json()
last_170=data["bars"][-170:]
closing_list=[]
for bar in last_170:
    closing_list.append(bar["c"])

signal=0
# Sell=1 

while True:
    try:
        response = requests.get(
            Quotes_URL,
            headers=HEADERS
        )
        if response.status_code==200:
            data=response.json()
            closing_list.append(data['quote']['ap'])
            closing_list.pop(0)
            SMA_170=sum(closing_list)/len(closing_list)
            SMA_25=sum(closing_list[-25:])/len(closing_list[-25:])
            print(f"SMA_170: {SMA_170}")
            print(f"SMA_25: {SMA_25}")
            if SMA_25>SMA_170 and signal==0:
                signal=1
                orders={
                    "symbol":"SPY",
                    "qty":1,
                    "side":"buy",
                    "type":"market",
                    "time_in_force":"day"
                }
                response=requests.post("https://paper-api.alpaca.markets/v2/orders",headers=HEADERS,json=orders)
                if response.status_code!=200:
                    print("Error occured")
                else:    
                    print("Buy order placed")
            elif SMA_25<SMA_170 and signal==1:
                signal=0
                orders={
                    "symbol":"SPY",
                    "qty":1,
                    "side":"sell",
                    "type":"market",
                    "time_in_force":"day"
                }
                response=requests.post("https://paper-api.alpaca.markets/v2/orders",headers=HEADERS,json=orders)
                if response.status_code!=200:
                    print("Error occured")
                else:    
                    print("Sell order placed")
            else:
                print("Maintaining position")
        time.sleep(60)

            
    except KeyboardInterrupt:
        print("Terminating process: Shutting down")
        break

