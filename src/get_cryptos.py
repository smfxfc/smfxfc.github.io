#! python3

"""Get latest cryptocurrency prices from Binance."""

import json
import re
import requests

CRYPTO_PAGE = "crypto/cryptos.md"
BASE_URL = "https://smfxfc.github.io/crypto/"
KEY = "https://api.binance.com/api/v3/ticker/price?symbol="

tokens = ["ETH", "LUNA", "XNO", "LINK", "AVAX"]

html = "\n"
for token in tokens:

    url = KEY + token + "USDT"
    info = requests.get(url)
    info = info.json()
    price = float(info["price"])
    site_url = f"[{token}]({BASE_URL}{token.lower()}.html)"

    if token == "LUNA":
        html += f"{site_url}: ${price:.2f} RIP :'(\n\n"
    else:
        html += f"{site_url}: ${price:.2f}\n\n"

with open(CRYPTO_PAGE, "r") as existing_page:
    previous_content = existing_page.read()

new_content = re.sub(
    r"(?<=<!\-\-BEGINCRYPTOINPUT\-\->)[\s\S]*(?=<!\-\-ENDCRYPTOINPUT\-\->)",
    f"{html}",
    previous_content,
)

with open(CRYPTO_PAGE, "w") as new_page:
    new_page.write(new_content)
