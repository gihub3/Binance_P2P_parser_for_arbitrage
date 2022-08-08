from parsers import *
from CONSTANTS import BANKS_EN_RUS, ALL_ASSET_COUPLES


def make_total_data_array(fiat):
    total_array = []
    for bank in BANKS_EN_RUS.keys():
        for asset_couple in ALL_ASSET_COUPLES:
            get_operation_info(*asset_couple, fiat)


def get_operation_info(from_asset, to_asset, fiat, bank=BANKS_EN_RUS.keys()):
    from_asset_info = get_asset_info(from_asset, fiat, "BUY", pay_types=bank)
    to_asset_info = get_asset_info(to_asset, fiat, "BUY", pay_types=bank)
    exchange_price = get_symbol_price(from_asset, to_asset)

    # return "Binance", " ", from_asset, to_asset, bank, bank,
    pass




