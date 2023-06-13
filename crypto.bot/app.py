
import telebot

from extensions import ConvertionException, CryptoConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ["start", "help"])
def help(message: telebot.types.Message):
    text= 'Что бы начать работу, введите команду в следующем формате:\n<имя валюты>\n<в какую валюту перевести> ' \
          '\n<количество переводимой валюты> \nУвидеть список доступных валют: "/values"'
    bot.reply_to(message, text)


@bot.message_handler(commands = ["values"])
def values(message: telebot.types.Message):
    text= "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Ошибка в вводе параметров.')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, "Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f'Цена {amount} {quote}ов  - {total_base} {base}ов'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)