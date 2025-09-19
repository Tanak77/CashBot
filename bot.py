import telebot
import config
from extensions import APIException, CurrencyConverter, CURRENCIES

# Создание экземпляра бота с использованием токена из config.py
bot = telebot.TeleBot(config.TOKEN)

# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = """
💱 *Конвертер валют* 

Для получения курса валют отправьте сообщение в формате:
*<валюта1> <валюта2> <количество>*

*Примеры использования:*
USD RUB 100 - Сколько стоит 100 долларов в рублях
EUR USD 50 - Сколько стоит 50 евро в долларах
RUB EUR 1000 - Сколько стоит 1000 рублей в евро

*Доступные команды:*
/start - запуск бота
/help - показать это сообщение
/values - показать список доступных валют
"""

    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# Обработчик команды /values
@bot.message_handler(commands=['values'])
def handle_values(message):
    text = "Доступные валюты:\n\n"
    for code, name in CURRENCIES.items():
        text += f"• {code} - {name}\n"
    bot.send_message(message.chat.id, text)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        # Разделение текста сообщения на части и приведение к верхнему регистру
        parts = message.text.upper().split()

        # Проверка правильности формата запроса
        if len(parts) != 3:
            raise APIException("Неверный формат. Нужно: <валюта1> <валюта2> <количество>")

        base, quote, amount = parts

        # Проверяем, что введенные валюты существуют
        if base not in CURRENCIES:
            raise APIException(f"Неизвестная валюта: {base}")
        if quote not in CURRENCIES:
            raise APIException(f"Неизвестная валюта: {quote}")

        # Выполнение конвертации валют
        result = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(message.chat.id, f"{amount} {base} = {result} {quote}")

    # Обработка ожидаемых ошибок (неправильный ввод пользователя)
    except APIException as e:
        bot.send_message(message.chat.id, f"❌Ошибка: {str(e)}")
    # Обработка непредвиденных ошибок
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️Произошла ошибка: {str(e)}")

# Запуск бота
bot.polling()