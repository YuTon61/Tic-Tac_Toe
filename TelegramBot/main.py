import telebot
from сonfig import keys, TOKEN
from extensions import APIException, Converter


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    #@bot.message_handler()
    #def bot_hi(message: telebot.types.Message):
    #    bot.send_message(message.chat.id, "Money, Money, Money Must Be Funny!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def bot_help(message: telebot.types.Message):
    text = "Для получения кросскурса валют введите следующую команду:\n\
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n\
Для получения списка доступных валют введите следующую команду: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def bot_keys(message: telebot.types.Message):
    text = "Доступны валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def bot_convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException(f"Неверное количество параметров: '{message.text}'")
        quote, base, amount = values
        total_base = Converter.get_price(base, quote, amount)
    except APIException as ae:
        bot.send_message(message.chat.id, f"Ошибка пользователя:\n '{ae}'")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка сервера:\n '{e}'")
    else:
        text = f"Цена '{amount}' '{quote}' в '{base}' = {total_base * float(amount)}"
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    print_hi('Telegram Bot')

    bot.polling()
