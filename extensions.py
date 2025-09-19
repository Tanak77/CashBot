import requests
import json
from config import API_KEY  # Добавляем импорт API_KEY

# Пользовательские исключения для обработки ошибок API
class APIException(Exception):
    pass

# Класс для конвертации валют
class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f"Нельзя конвертировать {base} в самого себя")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Количество должно быть числом: {amount}")

        # Формирование URL для запроса к API
        url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"

        try:
            # Отправка GET-запроса к API
            response = requests.get(url)
            # Парсинг JSON-ответа от сервера
            data = json.loads(response.text)

            # Проверка наличия ошибки в ответе API
            if 'error' in data:
                raise APIException(f"Ошибка API: {data['description']}")

            # Получение курсов валют из ответа
            rates = data['rates']

            # Проверка существования запрошенных валют
            if base not in rates:
                raise APIException(f"Неизвестная валюта: {base}")
            if quote not in rates:
                raise APIException(f"Неизвестная валюта: {quote}")

            # Конвертация валюты через USD (базовая валюта API)
            result = (amount / rates[base]) * rates[quote]
            return round(result, 2)

        # Обработка ошибок при запросе к API
        except Exception as e:
            raise APIException(f"Ошибка при получении данных: {str(e)}")


# Cписок валют
CURRENCIES = {
    'USD': 'Доллар США',
    'EUR': 'Евро',
    'RUB': 'Российский рубль',
    'GBP': 'Британский фунт',
    'JPY': 'Японская иена',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'HKD': 'Гонконгский доллар',
    'NZD': 'Новозеландский доллар',
    'SEK': 'Шведская крона',
    'KRW': 'Южнокорейская вона',
    'SGD': 'Сингапурский доллар',
    'NOK': 'Норвежская крона',
    'MXN': 'Мексиканское песо',
    'INR': 'Индийская рупия',
    'BRL': 'Бразильский реал',
    'ZAR': 'Южноафриканский рэнд',
    'TRY': 'Турецкая лира'
}