import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    #bot.send_message(message.chat.id, 'ello')
    text = 'Bot is online. \n <currency name> <convert into currency> <amount> \n check currencies: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Currencies:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Parameters error.')
        
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'User error.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Command error.\n{e}')
    else:
        text = f'{amount} {quote} is {float(amount)*total_base} {base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)