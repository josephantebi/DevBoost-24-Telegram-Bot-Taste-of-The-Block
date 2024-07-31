import logging

from telebot import types

from shared.shared_resource import shared_resource

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

restaurant_db = shared_resource.get_restaurant_db()
bot = shared_resource.get_bot()


def process_create_restaurant(message):
    new_restaurant = {'user_id': message.chat.id}
    return process_restaurant_name_step(message, new_restaurant)


def process_restaurant_name_step(message, restaurant):
    logger.info(f"=Inserting restaurant name: {message.text} #{message.chat.id}/{message.from_user.username!r}")
    restaurant['name'] = message.text
    msg = bot.reply_to(message, 'Please provide some description for your restaurant.')
    bot.register_next_step_handler(msg, process_restaurant_description_step, restaurant)


def process_restaurant_description_step(message, restaurant):
    logger.info(f"=Inserting restaurant description: {message.text} #{message.chat.id}/{message.from_user.username!r}")
    restaurant['description'] = message.text
    msg = bot.reply_to(message, 'What is the category of your restaurant.')
    bot.register_next_step_handler(msg, process_restaurant_category_step, restaurant)


def process_restaurant_category_step(message, restaurant):
    logger.info(f"=Inserting restaurant category: {message.text} #{message.chat.id}/{message.from_user.username!r}")
    restaurant['category'] = message.text
    chat_id = message.chat.id
    res = restaurant_db.add(restaurant)
    logger.info(f"=Done inserting restaurant {restaurant['name']} #{message.chat.id}/{message.from_user.username!r}")
    bot.send_message(chat_id, f'Creating {res['name']} done :)')


def show_restaurants():
    pass


def edit_restaurant(message):
    keyboard = types.InlineKeyboardMarkup()
    add_dish_button = types.InlineKeyboardButton(
        text="Add new dish",
        callback_data="add_dish"
    )
    edit_dish_button = types.InlineKeyboardButton(
        text="Edit a dish",
        callback_data="edit_dish"
    )
    keyboard.add(add_dish_button)
    keyboard.add(edit_dish_button)

    bot.send_message(message.chat.id, "Options:", reply_markup=keyboard)


def handle_add_dish(message):
    msg = bot.reply_to(message, 'Please provide a name for the dish.')
    bot.register_next_step_handler(msg, process_dish_name_step)


def process_dish_name_step(message):
    logger.info(f"=Inserting dish name: {message.text} #{message.chat.id}/{message.from_user.username!r}")
    dish = {'name': message.text}
    msg = bot.reply_to(message, 'Please provide a description for the dish.')
    bot.register_next_step_handler(msg, process_dish_description_step, dish)


def process_dish_description_step(message, dish):
    logger.info(f"=Inserting dish description: {message.text} #{message.chat.id}/{message.from_user.username!r}")
    dish['description'] = message.text
    msg = bot.reply_to(message, 'What is the price of the dish?')
    bot.register_next_step_handler(msg, process_dish_price_step, dish)


def process_dish_price_step(message, dish):
    try:
        price = float(message.text)
        dish['price'] = price
    except ValueError:
        bot.reply_to(message, 'Invalid price format. Please enter a numerical value.')
        return process_dish_price_step(message, dish)

    chat_id = message.chat.id

    res = restaurant_db.add_dish(chat_id, dish)
    logger.info(f"=Done inserting dish {dish['name']} #{message.chat.id}/{message.from_user.username!r}")
    bot.send_message(chat_id, f'Adding dish {res["name"]} done :)')
