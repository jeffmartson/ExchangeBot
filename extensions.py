import requests
import json


class APIException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            url = f"https://min-api.cryptocompare.com/data/price"
            params = {
                "fsym": quote,
                "tsyms": base
            }
            response = requests.get(url, params=params)
            data = response.json()

            if base not in data:
                raise APIException(f"Курс для валюты {base} не найден.")

            price = data[base]
        except requests.RequestException as e:
            raise APIException(f"Ошибка запроса к API: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            raise APIException(f"Ошибка при обработке данных: {e}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Некорректное количество криптовалюты")

        total_base = price * amount
        return total_base

    @staticmethod
    def get_top_cryptos():
        try:
            url = "https://min-api.cryptocompare.com/data/top/totalvolfull"
            params = {
                "limit": 20,
                "tsym": "USD"
            }
            response = requests.get(url, params=params)
            data = response.json()
            cryptos = [f"{coin['CoinInfo']['FullName']} ({coin['CoinInfo']['Name']})" for coin in data["Data"]]
        except requests.RequestException as e:
            raise APIException(f"Ошибка запроса к API: {e}")
        except (json.JSONDecodeError, KeyError) as e:
            raise APIException(f"Ошибка при обработке данных: {e}")

        return cryptos
