#! python3

"""Get latest cryptocurrency prices from Binance."""

import json
import requests
  
key = "https://api.binance.com/api/v3/ticker/price?symbol="
  
tokens = ["ETH", "LUNA", "NANO", "LINK", "AVAX"]
  
for token in tokens:
    
    url = key+token+"USDT"
    info = requests.get(url)
    info = info.json()
    
    print(f"{token}: {info['price']}")