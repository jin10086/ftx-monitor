import ccxt
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

ftx = ccxt.ftx()


def _public_get_futures_future_name_stats(name):
    result = ftx.public_get_futures_future_name_stats(name)
    result = result["result"]
    result["name"] = name["future_name"]
    return result


def get_future_stats(names):
    with ThreadPoolExecutor() as executor:
        return executor.map(_public_get_futures_future_name_stats, names)


def get_perpetual(futures):
    """获取永续资金率"""
    perpetuals = [i for i in futures if i["perpetual"]]
    perpetual_names = [{"future_name": i["name"]} for i in perpetuals]
    nextFundingRate_data = get_future_stats(perpetual_names)
    nextFundingRate_data = sorted(
        nextFundingRate_data, key=lambda k: abs(k["nextFundingRate"]), reverse=True
    )
    for i in nextFundingRate_data:
        del i["openInterest"]
        del i["volume"]
    return nextFundingRate_data


def get_btc_move_diff(futures):
    "获取各个btc move的差价"
    perpetuals = [i for i in futures if i["type"] == "move"]
    perpetual_names = [{"future_name": i["name"]} for i in perpetuals]
    strikePrices = get_future_stats(perpetual_names)
    strikePrices = {i["name"]: i for i in strikePrices}
    btc_moves = []
    for i in perpetuals:
        name = i["name"]
        if strikePrices[name].get("strikePrice", False):
            c = round(i["index"], 4)  # 指数成分市场的平均市价
            mark = i["mark"]  # 期货标记价格
            strikePrice = round(strikePrices[name]["strikePrice"], 4)  # 到期日开始时标的价格
            diff = round(abs(abs(c - strikePrice) - mark), 4)
            print(f"{name}: 行权价:{strikePrice}, BTC指数价:{c}, move价格:{mark},差价:{diff}")
            btc_moves.append(
                {
                    "index": c,
                    "mark": mark,
                    "strikePrice": strikePrice,
                    "diff": diff,
                    "name": name,
                }
            )
    return sorted(btc_moves, key=lambda k: k["diff"], reverse=True)


def get_future_diff(futures):
    """现货与期货的差异"""
    futures = [
        i for i in futures if i["type"] == "future" and "HASH" not in i["name"]
    ]  # 季度合约
    markets = ftx.load_markets()
    future_diff = []
    for i in futures:
        name = i["name"]
        spot_name = name.split("-")[0] + r"/USD"
        if markets.get(spot_name, False):
            spot_price = markets[spot_name]["info"]["price"]
            diff = round(abs(i["mark"] - spot_price), 2)
            rate = str(round((diff / spot_price) * 100, 3)) + "%"
            print(f"name:{name},期货价:{i['mark']},现货价:{ spot_price},差价:{diff},差价%:{rate}")
            future_diff.append(
                {
                    "name": name,
                    "mark": i["mark"],
                    "spot_price": spot_price,
                    "diff": diff,
                    "rate": rate,
                }
            )
    return sorted(future_diff, key=lambda k: k["diff"], reverse=True)


def main():
    futures = ftx.public_get_futures()["result"]
    future_diff = get_future_diff(futures)
    move_diff = get_btc_move_diff(futures)
    perpetual = get_perpetual(futures)[:20]

    with open("future_diff.json", "w") as f:
        f.write(json.dumps(future_diff))
    with open("move_diff.json", "w") as f:
        f.write(json.dumps(move_diff))
    with open("perpetual.json", "w") as f:
        f.write(json.dumps(perpetual))


if __name__ == "__main__":
    main()
