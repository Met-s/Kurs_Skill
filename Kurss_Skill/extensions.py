import requests
import json
from tok_en import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        if quote == base:
            raise APIException(
                f"Невозможно перевести одинаковые валюты "
                f"{base} !")
        if float(amount) <= 0:
            raise APIException('Количество валюты должно быть больше нуля')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту {quote} !')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту {base} !')

        try:
            amount = amount
        except ValueError:
            raise APIException(f'Не правильно введено количество '
                               f'{amount} !')

        r = requests.get(f'https://v6.exchangerate-api.com/v6'
                         f'/c94bc54473582e54e7bb0082/pair/'
                         f'{quote_ticker}/{base_ticker}')
        total_base = round(float(json.loads(r.content)["conversion_rate"]), 2)

        return total_base
