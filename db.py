from pymongo import MongoClient

from entities.Dish import Dish
from entities.Restaurant import Restaurant


class RestaurantDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.get_database("taste_of_the_block_bot")
        self.restaurants = self.db.get_collection("restaurants")
        self.restaurants.create_index("user_id", unique=True)

    def add_restaurant(self, restaurant: Restaurant):
        self.restaurants.insert_one({
            "user_id": restaurant.user_id,
            "name": restaurant.name,
            "category": restaurant.category,
            "description": restaurant.description,
            "menu": "json(restaurant.menu)"
        })
        return self.restaurants.find_one({'user_id': restaurant.user_id})


