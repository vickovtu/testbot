import requests


# https://exmo.com/ru/api#/public_api


def get_btc():
    url = 'https://api.exmo.com/v1/ticker/'
    price = requests.get(url).json()['BTC_USD']['sell_price']
    #  price = requests.get(url).json()
    #  print(price)
    return f'{round(float(price))} usd'


def get_usd_private():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    price = requests.get(url).json()[0]['buy']
    return f'{float(price)} uah'


print(get_btc())
