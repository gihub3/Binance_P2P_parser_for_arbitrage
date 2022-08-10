from parsers import *
from CONSTANTS import BANKS_EN_RUS, ALL_ASSET_COUPLES, OPERATION_TYPES, SYMBOLS
import asyncio


def calculate_profit(bank_amount, from_asset_p2p, to_asset_p2p, exchange_price, ratio=1):
    amount_after_operation = (bank_amount / from_asset_p2p) * (exchange_price ** ratio) * to_asset_p2p

    return bank_amount - amount_after_operation


def get_user_url(user_id):
    url = "https://p2p.binance.com/ru/advertiserDetail?advertiserNo="

    return url + user_id


def make_total_data_array(fiat, bank_amount):
    total_array = []
    all_params_array = []

    for symbol in SYMBOLS:
        all_params_array.append(form_symbol_price_params(symbol))

    for operation_type in OPERATION_TYPES:
        for bank in BANKS_EN_RUS.keys():
            for asset_couple in ALL_ASSET_COUPLES:
                all_params_array += get_all_params(
                    *asset_couple, fiat, OPERATION_TYPES[operation_type], bank
                )
    start_time = time.time()

    asyncio.run(load_data(all_params_array))

    end_time = time.time()
    print(end_time - start_time)

    for idx in range((len(sorted(all_data, key=lambda s: s[0])) - 6) // 2):
        from_asset = all_data[2 * idx][1]
        to_asset = all_data[2 * idx + 1][1]
        if from_asset["asset"] + to_asset["asset"] in SYMBOLS:
            cur_symbol = from_asset["asset"] + to_asset["asset"]
            ratio = 1
        else:
            cur_symbol = to_asset["asset"] + from_asset["asset"]
            ratio = -1
        analytics = get_analytics(bank_amount, from_asset, to_asset,
                                  calculate_profit(
                                      bank_amount,
                                      float(from_asset["price"]),
                                      float(to_asset["price"]),
                                      all_symbols_data[cur_symbol],
                                      ratio=ratio
                                  ),
                                  list(OPERATION_TYPES.keys())[idx // 64])
        total_array.append(analytics)

    print(total_array)
    return total_array


def get_all_params(from_asset, to_asset, fiat, order_type, bank):
    from_asset_info = form_asset_info_params(from_asset, fiat, order_type[0], pay_types=[bank])
    to_asset_info = form_asset_info_params(to_asset, fiat, order_type[1], pay_types=[bank])

    return [from_asset_info, to_asset_info]


def get_analytics(bank_amount, from_info, to_info, profit, operation_type):
    from_price, to_price = "", ""

    if from_info["asset"] == to_info["asset"]:
        from_price, to_price = from_info["price"], to_info["price"]

    formatted_info = [
        "Binance",
        operation_type,
        from_info["asset"],
        to_info["asset"],
        from_info["payment_system"],
        to_info["payment_system"],
        "",
        "",
        from_price,
        to_price,
        f'=HYPERLINK("{get_user_url(from_info["user_id"])}"; "{from_info["user_nickname"]}")',
        f'=HYPERLINK("{get_user_url(to_info["user_id"])}"; "{to_info["user_nickname"]}")',
        profit / bank_amount * 100,
        profit
    ]

    return formatted_info


# make_total_data_array("RUB", 30000)
