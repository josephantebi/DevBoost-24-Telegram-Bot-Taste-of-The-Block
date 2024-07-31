import logging
import telebot

import bot_secrets
from db import RestaurantDB

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)


class SharedResource:
    def __init__(self):
        self.restaurant_db = RestaurantDB()
        self.logger = logging.getLogger(__name__)
        self.bot = telebot.TeleBot(bot_secrets.BOT_TOKEN)

    def get_restaurant_db(self):
        return self.restaurant_db

    def get_logger(self):
        return self.logger

    def get_bot(self):
        return self.bot


shared_resource = SharedResource()
