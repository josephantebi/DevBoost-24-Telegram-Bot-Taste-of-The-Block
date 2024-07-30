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
    telebot.types.BotCommand("/create_restaurant", "Create a new restaurant"),
    telebot.types.BotCommand("/edit_restaurant", "Edit your restaurant"),
    telebot.types.BotCommand("/remove_restaurant", "Remove restaurant"),
    telebot.types.BotCommand("/show_restaurants", "List all restaurants"),
    telebot.types.BotCommand("/load_demo", "Load demo restaurants data"),
    telebot.types.BotCommand("/my_cart", "Show my cart")
])


@bot.message_handler(commands=['start'])
def start(message):
    start_message = """
Welcome to Taste of The Block, here you can add your restaurant or buy something delicious ;)
These commands will help you:

/create_restaurant - Create a new restaurant
/edit_restaurant - Edit your restaurant
/remove_restaurant - Remove restaurant
/show_restaurants - List all restaurants
/load_demo - Load demo restaurants data
/my_cart - Show my cart
    """
    bot.send_message(message.chat.id, start_message)


@bot.message_handler(commands=['load_demo'])
def load_demo(message):
    taste_of_the_block = generate_from_json("restaurants.json")
    for res in taste_of_the_block.restaurants:
        pprint(res)
        restaurant_db.add_restaurant(res)
    bot.send_message(message.chat.id, "Demo data loaded successfully.")


@bot.message_handler(commands=['show_restaurants'])
def show_restaurants(message):
    restaurants = restaurant_db.restaurants.find()
    for restaurant in restaurants:
        restaurant_info = f"Restaurant name: {restaurant['name']}\n\n" \
                          f"{restaurant['description']}\n\n" \
                          f"Category: {restaurant['category']}"

        keyboard = types.InlineKeyboardMarkup()
        menu_button = types.InlineKeyboardButton(
            text="Menu",
            callback_data=f"menu_{restaurant['user_id']}"
        )
        keyboard.add(menu_button)

        bot.send_message(message.chat.id, restaurant_info, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
def show_menu(call):
    user_id = int(call.data.split("_")[1])
    restaurant = restaurant_db.restaurants.find_one({'user_id': user_id})
    if restaurant:
        restaurant_info = f"Restaurant name: {restaurant['name']}\n\n" \
                          f"{restaurant['description']}\n\n" \
                          f"Category: {restaurant['category']}"
        bot.send_message(call.message.chat.id, restaurant_info)

        if 'menu' in restaurant:
            dishes_msg = "These are the dishes we offer:"
            bot.send_message(call.message.chat.id, dishes_msg)
            for dish in restaurant['menu']:
                dish_info = f"Dish name: {dish['name']}\n\n" \
                            f"{dish['description']}\n\n" \
                            f"Price: {dish['price']}"
                bot.send_message(call.message.chat.id, dish_info)

        end_msg = "Thank you for choosing to view our restaurant. Hope to see you again soon 🤩"
        bot.send_message(call.message.chat.id, end_msg)


@bot.message_handler(commands=['create_restaurant'])
def create_restaurant(message):
    bot.send_message(message.chat.id, "Please choose a name for your restaurant.")
    logger.info(f"= Creating restaurant: #{message.chat.id}/{message.from_user.username!r}")


@bot.message_handler(func=lambda message: True)
def echo_message(message: telebot.types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text
    logger.info(f"= Add item: #{chat_id}/{username!r}: {text!r}")
    bot.send_message(chat_id, str(message))

logger.info("* Start polling...")
bot.infinity_polling()
logger.info("* Bye!")
