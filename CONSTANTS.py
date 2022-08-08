from itertools import combinations

CREDENTIALS_FILE = 'creds.json'

ASSETS = [
    "USDT",
    "BTC",
    "BUSD",
    "ETH"
]

combinations = list(combinations(ASSETS, 2))
ALL_ASSET_COUPLES = combinations + list(map(lambda x: x[::-1], combinations))

# BANKS_RUS = [
#     "Тинькофф",
#     "Росбанк",
#     "QIWI",
#     "ЮMoney"
# ]

BANKS_EN_RUS = {
    "Tinkoff": "Тинькофф",
    "Rosbank": "Росбанк",
    "QIWI": "QIWI",
    "YandexMoneyNew": "ЮMoney"
}

