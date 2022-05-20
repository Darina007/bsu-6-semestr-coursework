import telebot

import config
import gpt

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, config.message)


@bot.message_handler(content_types=['text'])
def start_message(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, gpt.create_chat_answer(message))


if __name__ == '__main__':
    bot.polling(none_stop=True)
