import logging
from pprint import pprint

import telebot
from telebot import types

import bot_secrets
from db import RestaurantDB
from utilities.generate import generate_from_json

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_secrets.BOT_TOKEN)

restaurant_db = RestaurantDB()

bot.set_my_commands([
    telebot.types.BotCommand("/crete_restaurant", "Create a new restaurant"),
    telebot.types.BotCommand("/edit_restaurant", "Edit your restaurant"),
    telebot.types.BotCommand("/remove_restaurant", "Remove restaurant"),
    telebot.types.BotCommand("/show_restaurants", "List all restaurants"),
    telebot.types.BotCommand("/my_cart", "Show my cart")
])


@bot.message_handler(commands=['start'])
def start(message):
    # keyboard = types.InlineKeyboardMarkup()
    #
    # my_restaurant = types.InlineKeyboardButton(text="My Restaurant", callback_data="my_restaurant")
    # find_restaurant = types.InlineKeyboardButton(text="Find Restaurants", callback_data="find_restaurant")
    #
    # keyboard.add(my_restaurant)
    # keyboard.add(find_restaurant)

    # bot.send_message(message.chat.id, "Wellcome to Taste of The Block", reply_markup=keyboard)

    taste_of_the_block = generate_from_json("restaurants 2.json")

    # pprint(taste_of_the_block.restaurants)
    for res in taste_of_the_block.restaurants:
        pprint(res)
        restaurant_db.add_restaurant(res)

    start_message = """
Wellcome to Taste of The Block, here you can add your restaurant or buy something delicious ;)
These commands will help you:

/create_restaurant - Create a new restaurant
/edit_restaurant - Edit your restaurant
/remove_restaurant - Remove restaurant
/show_restaurants - List all restaurants
/my_cart - Show my cart
    """

    bot.send_message(message.chat.id, start_message)


@bot.message_handler(commands=['create_restaurant'])
def create_restaurant(message):
    bot.send_message(message.chat.id, "Please choose a name for your restaurant.")
    logger.info(f"= Creating restaurant: #{message.chat.id}/{message.username!r}")


# Handle all other messages with content_type 'text'
@bot.message_handler(func=lambda message: True)
def echo_message(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text

    logger.info(f"= Add item: #{chat_id}/{username!r}: {text!r}")

    # items = shopping_db.add_restaurant(chat_id, text)

    # msg = f"Added {text}, you currently have {len(items)}."

    # bot.reply_to(message, response)
    bot.send_message(chat_id, str(message))


logger.info("* Start polling...")
bot.infinity_polling()
logger.info("* Bye!")
