import json

from requests import post, get


def get_asset_info(asset, fiat, trade_type, pay_types=None, trans_amount=' ',
                   merchant_check=False, page=1, publisher_type=None, row=1):
    if pay_types is None:
        pay_types = []
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    params = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": merchant_check,
        "page": page,
        "payTypes": pay_types,
        "publisherType": publisher_type,
        "rows": row,
        "tradeType": trade_type,
        "transAmount": trans_amount
    }

    response = post(url, json=params)
    print(response.url)

    print(response)

    if response:
        print(response.json())
        with open("data.json", 'wt') as file:
            json.dump(response.json(), file)

    needed_data = response.json()["data"][0]

    return needed_data["adv"]["price"], needed_data["adv"]["tradeMethods"][0]["identifier"], \
           needed_data["advertiser"]["nickName"], needed_data["advertiser"]["userNo"]


get_asset_info("USDT", "RUB", "BUY")


def get_symbol_price(from_asset, to_asset):
    url = 'https://binance.com/api/v3/ticker/price'
    params = {
        "symbol": from_asset + to_asset
    }

    response = get(url, params=params)
    print(response.url)

    print(response)

    if response:
        print(response.json())
        with open("convert.json", 'wt') as file:
            json.dump(response.json(), file)

    return response.json()["price"]
