import logging

import telebot
from telebot import types

from shared.shared_resource import shared_resource
from service import restaurant_srevice, load_demo_restaurants

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

restaurant_db = shared_resource.get_restaurant_db()
bot = shared_resource.get_bot()


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
    load_demo_restaurants.load_demo()
    bot.send_message(message.chat.id, "Demo data loaded successfully.")


@bot.message_handler(commands=['show_restaurants'])
def show_restaurants(message):
    #TODO: What if there is no restaurants ?
    restaurants = restaurant_db.find_all()
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
    logger.info(f"= Creating restaurant: #{message.chat.id}/{message.from_user.username!r}")
    msg = bot.reply_to(message, "Please choose a name for your restaurant.")
    bot.register_next_step_handler(msg, restaurant_srevice.process_create_restaurant)


@bot.message_handler(commands=['edit_restaurant'])
def edit_restaurant(message):
    logger.info(f"= Editing restaurant: #{message.chat.id}/{message.from_user.username!r}")
    restaurant_srevice.edit_restaurant(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_option(call):
    if call.data == "add_dish":
        restaurant_srevice.handle_add_dish(message=call.message)
    elif call.data == "edit_dish":
        pass


logger.info("* Start polling...")
bot.infinity_polling()
logger.info("* Bye!")
