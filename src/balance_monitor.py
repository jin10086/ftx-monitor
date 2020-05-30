import requests
import json
from datetime import datetime

btc_address = "1G47mSr3oANXMafVrR8UC4pzV7FEAzo3r9"
eth_address = "0x2FAF487A4414Fe77e2327F0bf4AE2a264a776AD2"

ERC_20_TOKENS = ["TUSD", "USDC", "PAX", "BUSD", "USDT", "HUSD"]


def getBTCBalance():
    print("get btc balance...")
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{btc_address}/balance"
    z1 = requests.get(url)
    balance = z1.json()["balance"]
    return balance / 1e8


def getBalance():
    print("get eth balance...")
    url = f"https://api.ethplorer.io/getAddressInfo/{eth_address}?apiKey=nyfdv4926Oop96"
    z1 = requests.get(url)
    c1 = {}
    c1["ETH"] = z1.json()["ETH"]["balance"]
    for token in z1.json()["tokens"]:
        symbol = token["tokenInfo"]["symbol"]
        if symbol in ERC_20_TOKENS:
            decimals = int(token["tokenInfo"]["decimals"])
            balance = token["balance"] / pow(10, decimals)
            c1[symbol] = balance
    btc = getBTCBalance()
    c1["BTC"] = btc
    c1["updatetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # "ETH", "TUSD", "USDC", "PAX", "BUSD", "USDT", "HUSD", "BTC"
    c2 = [
        c1["updatetime"],
        c1["ETH"],
        c1["TUSD"],
        c1["USDC"],
        c1["PAX"],
        c1["BUSD"],
        c1["USDT"],
        c1["HUSD"],
        c1["BTC"],
    ]
    with open("balance.json", "r") as f:
        old_data = json.loads(f.read())

    old_data.append(c2)

    with open("balance.json", "w") as f:
        f.write(json.dumps(old_data))


if __name__ == "__main__":
    getBalance()
