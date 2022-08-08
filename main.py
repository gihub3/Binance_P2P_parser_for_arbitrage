from requests import get

url = "https://p2p.binance.com/ru/advertiserDetail"
params = {
    "advertiserNo": "s128bce2116883c5da748ccea16e594a5"
}

r = get(url, params=params)
print(r)
print(r.url)
