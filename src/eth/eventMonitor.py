from web3 import Web3, WebsocketProvider
import json

w3 = Web3(
    WebsocketProvider("wss://mainnet.infura.io/ws/v3/cd42b3642f1441629f66000f8e544d5d")
)

with open("erc20.json") as f:
    erc20abi = json.loads(f.read())

comp = w3.eth.contract(
    address="0xc00e94Cb662C3520282E6f5717214004A7f26888", abi=erc20abi
)
a1 = comp.events.Transfer.createFilter(fromBlock="latest", toBlock="pending")

while True:
    c = a1.get_new_entries()
    for i in c:
        amount = i["args"]["amount"]
        amount = w3.fromWei(amount, "ether")
        if amount < 1000:  # 大于1000 alarm
            continue
        f = i["args"]["from"]
        to = i["args"]["to"]
        txhash = w3.toHex(i["transactionHash"])
        print(
            f"""发现超过1000COMP的转账!
        发现者:{f}
        接收者:{to}
        金额:{amount}
        txhash:{txhash}
        """
        )
