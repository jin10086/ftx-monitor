from web3 import Web3, WebsocketProvider
import json
from sendMail import sendMail
from diskcache import Index

result = Index("data/result")

import os, sys, time

w3 = Web3(
    WebsocketProvider(
        "wss://mainnet.infura.io/ws/v3/cd42b3642f1441629f66000f8e544d5d",
        websocket_timeout=30,
    )
)

with open("erc20.json") as f:
    erc20abi = json.loads(f.read())

comp = w3.eth.contract(
    address="0xc00e94Cb662C3520282E6f5717214004A7f26888", abi=erc20abi
)


def go():
    a1 = comp.events.Transfer.createFilter(fromBlock="latest", toBlock="pending")
    print("开始检测大于500的comp转账")
    while True:
        c = a1.get_new_entries()
        for i in c:
            amount = i["args"]["amount"]
            amount = w3.fromWei(amount, "ether")
            if amount < 500:  # 大于1000 alarm
                continue
            f = i["args"]["from"]
            if f == "0x8248C5709b0835366821d0cAe83bdB7e2cf66a53":
                continue
            to = i["args"]["to"]
            txhash = w3.toHex(i["transactionHash"])
            msg = f"""发送者:{f}

接收者:{to}

金额:{amount}

txhash:https://cn.etherscan.com/tx/{txhash}
"""
            print("发送邮件中...")
            if "txs" in result:
                txhashs = result["txs"]
                if txhash not in txhashs:
                    txhashs.append(txhash)
                    # sendMail(
                    #     "发现超过500COMP的转账!", msg, ["igaojin@qq.com", "woody168@gmail.com"]
                    # )
                    print(msg)

            else:
                txhashs = [txhash]
                result["txs"] = txhashs
                # sendMail(
                #     "发现超过500COMP的转账!", msg, ["igaojin@qq.com", "woody168@gmail.com"]
                # )
                print(msg)


def main():
    print("AutoRes is starting")

    go()

    executable = sys.executable
    args = sys.argv[:]
    print(args)
    args.insert(0, sys.executable)

    time.sleep(1)
    print("Respawning")
    os.execvp(executable, args)


if __name__ == "__main__":
    main()
