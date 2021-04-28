import requests
import json
from сonfig import keys, ACCESS_KEY


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if quote == base:
            raise APIException(f"Невозможно конвертировать валюту в себя '{quote} -> {base}'")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Невозможно обработать эту валюту '{quote}'")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Невозможно перевести '{quote}' в '{base}'")

        try:
            amount_ticker = float(amount)
        except ValueError:
            raise APIException(f"Неверно указано количество валюты '{amount}'")

        #https://exchangeratesapi.io/
        #http://api.exchangeratesapi.io/v1/latest?access_key=c566ebd83272a21f36345a48487fe862&symbols=USD,RUB
        #{"success":true,"timestamp":1619613844,"base":"EUR","date":"2021-04-28","rates":{"USD":1.207183,"RUB":90.107762}}

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={ACCESS_KEY}&symbols={keys[quote]},{keys[base]}")
        d = json.loads(r.content)
        return d["rates"][keys[base]] / d["rates"][keys[quote]]
