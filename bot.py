import logging

import telebot

import bot_secrets
from db import ShoppingDB

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.BOT_TOKEN)

shopping_db = ShoppingDB()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    logger.info(f"> Start chat #{chat_id}. username: {username}")
    bot.send_message(chat_id, "Enter your shopping list items")


# Handle all other messages with content_type 'text'
@bot.message_handler(func=lambda message: True)
def echo_message(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    logger.info(f"= Add item: #{chat_id}/{username!r}: {text!r}")

    items = shopping_db.add_item(chat_id, text)

    msg = f"Added {text}, you currently have {len(items)}."

    # bot.reply_to(message, response)
    bot.send_message(chat_id, msg)


logger.info("* Start polling...")
bot.infinity_polling()
logger.info("* Bye!")
