import telebot
from config import token
from extensions import Exchange, APIException

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = "Привет! Я Бот-Конвертер криптовалюты в USD и обратно. Введите команду в формате: \n\n<криптовалюта> <валюта> <количество>"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    cryptos = Exchange.get_top_cryptos()
    text = "Доступные криптовалюты (первые 20 по объему торгов):\n\n" + "\n".join(cryptos)
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message):
    try:
        user_input = message.text.split()

        if len(user_input) != 3:
            raise APIException("Введите команду в правильном формате: <криптовалюта> <валюта> <количество>")

        base, quote, amount = user_input
        total_base = Exchange.get_price(base, quote, amount)
        # Форматирование строки с выводом до 5 знаков после десятичной точки, без округления
        formatted_total_base = f'{total_base:.5f}'
        text = f"Конвертация {base} в {quote}\n{amount} {base} = {formatted_total_base} {quote}"
        bot.send_message(message.chat.id, text)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя: {e}")
    except Exception as e:
        bot.reply_to(message, f"Что-то пошло не так: {e}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
