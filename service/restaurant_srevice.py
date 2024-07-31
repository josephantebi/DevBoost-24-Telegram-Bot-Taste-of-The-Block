from shared.shared_resource import shared_resource

restaurant_db = shared_resource.get_restaurant_db()
bot = shared_resource.get_bot()


#TODO: add log
def process_restaurant_name_step(message, restaurant):
    restaurant['name'] = message.text
    msg = bot.reply_to(message, 'Please provide some description for your restaurant.')
    bot.register_next_step_handler(msg, process_restaurant_description_step, restaurant)


def process_restaurant_description_step(message, restaurant):
    restaurant['description'] = message.text
    msg = bot.reply_to(message, 'What is the category of your restaurant.')
    bot.register_next_step_handler(msg, process_restaurant_category_step, restaurant)


def process_restaurant_category_step(message, restaurant):
    restaurant['category'] = message.text
    chat_id = message.chat.id
    res = restaurant_db.add_restaurant(restaurant)
    bot.send_message(chat_id, f'Creating {res['name']} done :)')
